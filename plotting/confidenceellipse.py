
# From https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html

if __name__=='__main__':

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    import matplotlib.transforms as transforms

    def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
        """
        Create a plot of the covariance confidence ellipse of `x` and `y`

        See how and why this works: https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html

        This function has made it into the matplotlib examples collection:
        https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py

        Or, once matplotlib 3.1 has been released:
        https://matplotlib.org/gallery/index.html#statistics

        I update this gist according to the version there, because thanks to the matplotlib community
        the code has improved quite a bit.

        Parameters
        ----------
        x, y : array_like, shape (n, )
            Input data.

        ax : matplotlib.axes.Axes
            The axes object to draw the ellipse into.

        n_std : float
            The number of standard deviations to determine the ellipse's radiuses.

        Returns
        -------
        matplotlib.patches.Ellipse

        Other parameters
        ----------------
        kwargs : `~matplotlib.patches.Patch` properties
        """
        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        cov = np.cov(x, y)
        pearson = cov[0, 1 ] /np.sqrt(cov[0, 0] * cov[1, 1])
        # Using a special case to obtain the eigenvalues of this
        # two-dimensionl dataset.
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0),
                          width=ell_radius_x * 2,
                          height=ell_radius_y * 2,
                          facecolor=facecolor,
                          **kwargs)

        # Calculating the stdandard deviation of x from
        # the squareroot of the variance and multiplying
        # with the given number of standard deviations.
        scale_x = np.sqrt(cov[0, 0]) * n_std
        mean_x = np.mean(x)

        # calculating the stdandard deviation of y ...
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = np.mean(y)

        transf = transforms.Affine2D() \
            .rotate_deg(45) \
            .scale(scale_x, scale_y) \
            .translate(mean_x, mean_y)

        ellipse.set_transform(transf + ax.transData)
        return ax.add_patch(ellipse)
        # render plot with "plt.show()".