import numpy as np
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import nearest_pos_def, mean_off_diag, cov_to_corrcoef


class FixedUniverseSkaterState:
    """
    Represents a set of variables (keys) for which we maintain a running covariance estimate.
    """

    def __init__(self, keys, max_buffer=500):
        self.keys = list(keys)  # Keep keys in a consistent order
        self.keys_set = set(keys)
        self.staleness = 0  # Counts how many updates have passed without data for this universe
        self.longevity = 0  # Total number of updates this universe has been active
        self.f_state = {}  # State of the skater function
        self.running_cov = None  # Current covariance estimate
        self.running_mean = None  # Current mean estimate
        self.running_corr = None
        self.buffer = list()
        self.max_buffer = max_buffer
        self.cloned = False

    def update(self, x, f):
        if f.__closure__ is not None:
            raise ValueError("Function f should not be a closure.")
        x = dict(x)
        self.buffer.append(x)
        if len(self.buffer) > self.max_buffer:
            self.buffer.pop(0)
        y = [x[k] for k in self.keys]
        x_mean, x_cov, posterior_state = f(y=y, s=self.f_state)
        self.f_state = posterior_state
        self.running_cov = x_cov
        self.running_corr = cov_to_corrcoef(self.running_cov)
        self.running_mean = x_mean
        self.staleness = 0
        self.longevity += 1

    def clone_and_replay(self, key_subset:[str], f):
        """
           Reduce the universe to a subset of keys and re-run the buffer to bring the estimates up to date
        """
        # Clone
        clone = FixedUniverseSkaterState(keys=key_subset)

        # Replay
        clone.f_state = {}
        for x in self.buffer:
            x_subset = dict( [ (k,v) for k, v in x.items() if k in key_subset] )
            clone.update(x=x_subset, f=f)
        return clone

    def __str__(self):
        # Print nicely ...
        mean_off_diag_corr = mean_off_diag(self.running_corr)
        return f"Universe: {self.keys} staleness={self.staleness} longevity={self.longevity} mean_corr={mean_off_diag_corr}"


class SkaterCovariance():
    """
    Maintains running covariance estimates using supplied skater functions, handling dynamic keys.
    """

    def __init__(self, max_universes=10, max_staleness=50, min_longevity_for_clone=3):
        """
        Parameters
        ----------
        f : function
            Covariance skater function following precise package conventions.
        max_universes : int
            Maximum number of states to maintain.
        max_staleness : int
            Maximum allowed staleness before dropping a universe.
        """
        self.states = {}  # Mapping from universe index to FixedUniverseSkaterState instances
        self.x = None  # Most recent data point
        self.max_universes = max_universes
        self.max_staleness = max_staleness
        self.min_longevity_for_clone = min_longevity_for_clone   # Min longevity for split
        self.universe_counter = 0  # Unique ID for states

    def __str__(self):
        return f"SkaterCovariance with {len(self.states)} states"

    def update(self, x: dict, f):
        """
        Update running covariance estimates with a new data point.

        Parameters
        ----------
        x : dict
            Dictionary of keys and their observed values.
        """
        # Save the latest data point
        self.x = dict(x)
        x_keys_set = set(x.keys())

        # Update existing states
        for uni_ndx, fixed_uni_skater in list(self.states.items()):  # Iterate over a copy of the items

            if fixed_uni_skater.keys_set.issubset(x_keys_set):
                # FixedUniverseSkaterState can be updated easily
                fixed_uni_skater.update(x=x,f=f)
            else:
                # ... but maybe we clone (split) universe into two if the new data has enough overlap
                if not fixed_uni_skater.cloned and (fixed_uni_skater.longevity > self.min_longevity_for_clone):
                    intersect = fixed_uni_skater.keys_set.intersection(x_keys_set)
                    num_keys = len(fixed_uni_skater.keys_set)
                    import math
                    min_overlap_0 = 2
                    min_overlap_1 = int(math.ceil(math.sqrt(num_keys)))
                    min_overlap = max( max(max(min_overlap_1, 2), num_keys - 10), min_overlap_0)
                    if len(intersect) >= min_overlap:
                        # Clone the universe with the intersected keys
                        clone = fixed_uni_skater.clone_and_replay(key_subset=intersect,f=f)
                        self.states[uni_ndx].cloned = True
                        self.states[self.universe_counter] = clone
                        self.universe_counter += 1
                    else:
                        self.states[uni_ndx].staleness += 1
                        # Increment staleness if the new data can't really be used to update the universe usefully
                        fixed_uni_skater.staleness += 1
                else:
                    try:
                        self.states[uni_ndx].staleness += 1
                    except AttributeError:
                        print('whaat???')
                        raise ValueError("")

        # Remove stale states
        to_remove = [uni_ndx for uni_ndx, universe in self.states.items() if universe.staleness > self.max_staleness]
        for uni_ndx in to_remove:
            del self.states[uni_ndx]

        # Create new universe if necessary
        existing_universe_keysets = [u.keys_set for u in self.states.values()]
        if x_keys_set not in existing_universe_keysets:
            # Initialize a new universe
            fixed_uni_skater = FixedUniverseSkaterState(keys=x.keys())
            fixed_uni_skater.update(x=x,f=f)
            uni_ndx = self.universe_counter
            self.states[uni_ndx] = fixed_uni_skater
            self.universe_counter += 1

            # Enforce maximum number of states
            if len(self.states) > self.max_universes:
                # Remove the stalest universe with the least longevity
                stale_universes = sorted(
                    self.states.items(),
                    key=lambda item: (-item[1].staleness, item[1].longevity)
                )
                stalest_universe_ndx = stale_universes[0][0]
                del self.states[stalest_universe_ndx]

    def get_pairwise_cov(self, keys: [str] = None) -> pd.DataFrame:
        """
        Retrieve pairwise covariance estimates for the specified keys.

        Parameters
        ----------
        keys : list of str
            The keys (variables) for which to retrieve covariances.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing pairwise covariance estimates.
        """
        if keys is None:
            if self.x is None:
                raise ValueError("No keys provided and no data has been updated yet.")
            keys = list(self.x.keys())

        cov_matrix = pd.DataFrame(index=keys, columns=keys, dtype=float)

        # Compute pairwise covariances ... there has to be a better greedy algorithm here
        # (e.g. start with longest surviving universe and then look for the next longest surviving universe etc and tag pairs as done)
        for i, key_i in enumerate(keys):
            for key_j in keys[i:]:
                # Find states containing both keys, not stale, with longest longevity
                candidate_universes = [
                    universe for universe in self.states.values()
                    if universe.staleness == 0 and {key_i, key_j}.issubset(universe.keys_set)
                ]
                if candidate_universes:
                    # Use the universe with longest longevity
                    selected_universe = max(
                        candidate_universes, key=lambda u: u.longevity
                    )
                    keys_list = selected_universe.keys
                    idx_i = keys_list.index(key_i)
                    idx_j = keys_list.index(key_j)
                    cov = selected_universe.running_cov[idx_i][idx_j]
                    cov_matrix.at[key_i, key_j] = cov
                    cov_matrix.at[key_j, key_i] = cov
                else:
                    # Covariance not available
                    cov_matrix.at[key_i, key_j] = np.nan
                    cov_matrix.at[key_j, key_i] = np.nan

        return cov_matrix

    def get_cov(self, keys: [str] = None) -> pd.DataFrame:
        """
        Retrieve a full covariance matrix, ensuring positive definiteness.

        Parameters
        ----------
        keys : list of str
            The keys (variables) for which to retrieve the covariance matrix.

        Returns
        -------
        pd.DataFrame
            A positive definite covariance matrix.
        """
        pairwise_cov = self.get_pairwise_cov(keys=keys)

        # Compute the mean of the non-NaN off-diagonal elements
        off_diag_elements = pairwise_cov.where(~np.eye(pairwise_cov.shape[0], dtype=bool))
        fill_cov_value = off_diag_elements.stack().mean()  # Grand mean of non-NaN off-diagonal elements

        # Fill NaN values in the pairwise covariance matrix
        cov_matrix = pairwise_cov.fillna(fill_cov_value)

        cov_matrix = (cov_matrix + cov_matrix.T) / 2  # Ensure symmetry

        # Adjust to nearest positive-definite matrix
        cov_array = cov_matrix.values
        cov_array_pd = nearest_pos_def(cov_array)
        cov_matrix_pd = pd.DataFrame(
            cov_array_pd, index=cov_matrix.index, columns=cov_matrix.columns
        )
        return cov_matrix_pd

    def get_pairwise_corr(self, keys: [str] = None) -> pd.DataFrame:
        """
        Retrieve pairwise correlation estimates for the specified keys.

        Parameters
        ----------
        keys : list of str
            The keys (variables) for which to retrieve correlations.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing pairwise correlation estimates.
        """
        pairwise_cov = self.get_pairwise_cov(keys=keys)
        variances = pairwise_cov.values.diagonal()
        std_dev = np.sqrt(variances)
        # Handle division by zero
        std_dev[std_dev == 0] = np.nan
        corr_matrix = pairwise_cov.divide(std_dev, axis=0).divide(std_dev, axis=1)
        return corr_matrix

    def get_corr(self, keys: [str] = None) -> pd.DataFrame:
        """
        Retrieve a full correlation matrix.

        Parameters
        ----------
        keys : list of str
            The keys (variables) for which to retrieve the correlation matrix.

        Returns
        -------
        pd.DataFrame
            A correlation matrix with ones on the diagonal.
        """
        pairwise_corr = self.get_pairwise_corr(keys=keys)
        corr_matrix = pairwise_corr.fillna(0)
        corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Ensure symmetry
        np.fill_diagonal(corr_matrix.values, 1)  # Set diagonal to 1
        return corr_matrix
