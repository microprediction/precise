from precise.skatervaluation.portfoliocomparisonutil.portsuggestion import suggest_port_using_sample_cov
from pprint import pprint

# Recommend static portfolio function based on sampled port var using simulation


if __name__=='__main__':
    pprint(suggest_port_using_sample_cov(n_dim=500, n_anchor=600, n_true=1000, n_observed=250))







# Some results below...
# pprint(sample_var_suggestions(n_dim=20, n_draws=500, n_samples=200, n_anchor_samples=200))

result= [('weak_long_port', 0.3225309176379648),
 ('hrp_diag_weak_s5_long_port', 0.32500160253517624),
 ('hrp_weak_diag_s5_long_port', 0.32500160253517624),
 ('hrp_weak_weak_s5_long_port', 0.3250038781544728),
 ('schur_weak_weak_s5_g050_long_port', 0.32502478692426406),
 ('ppo_quad_long_port', 0.3250380273392608),
 ('ppo_vol_long_port', 0.3258167331319683),
 ('schur_weak_weak_s5_g100_long_port', 0.32581688954098414),
 ('diag_long_port', 0.33205243885571795),
 ('ppo_quad_port', 0.3326438106380653),
 ('unit_port', 0.3349498393460227),
 ('ppo_vol_port', 0.33494986527520165),
 ('equal_long_port', 0.335745305599477),
 ('schur_diag_diag_s5_g100_long_port', 0.3363809194609325),
 ('schur_diag_diag_s5_g050_long_port', 0.33638197292595123),
 ('hrp_diag_diag_s5_long_port', 0.3364297258865387),
 ('hrp_unit_diag_s5_port', 0.3388700847179224),
 ('hrp_unit_unit_s5_port', 0.3388741854001973),
 ('hrp_unit_weak_s5_port', 0.3388766198811776),
 ('schur_unit_unit_s5_g050_port', 0.3389499356908701),
 ('schur_unit_unit_s5_g100_port', 0.3391326320617823),
 ('ppo_sharpe_long_port', 0.3429217942272056),
 ('ppo_sharpe_port', 0.35920489677145645)]



#  pprint(sample_var_suggestions(n_dim=50, n_draws=500, n_samples=200, n_anchor_samples=200))

result = [('weak_long_port', 0.28201237175425664),
 ('ppo_quad_long_port', 0.28691596836621003),
 ('ppo_vol_long_port', 0.287586722563168),
 ('schur_weak_weak_s5_g100_long_port', 0.3000864943055388),
 ('schur_weak_weak_s5_g050_long_port', 0.30183489136014274),
 ('hrp_weak_diag_s5_long_port', 0.30322931421876953),
 ('hrp_diag_weak_s5_long_port', 0.3032299914427331),
 ('hrp_weak_weak_s5_long_port', 0.3032375945185192),
 ('ppo_quad_port', 0.3085125317831518),
 ('diag_long_port', 0.30865645216189663),
 ('ppo_sharpe_long_port', 0.30960958196423255),
 ('schur_diag_diag_s5_g050_long_port', 0.31177144296164805),
 ('schur_diag_diag_s5_g100_long_port', 0.3117813323186178),
 ('hrp_diag_diag_s5_long_port', 0.31193888671764347),
 ('equal_long_port', 0.3123120335469827),
 ('schur_unit_unit_s5_g100_port', 0.3126512980773186),
 ('hrp_unit_diag_s5_port', 0.3127047766040293),
 ('hrp_unit_unit_s5_port', 0.3127129478018668),
 ('schur_unit_unit_s5_g050_port', 0.3127165635048669),
 ('hrp_unit_weak_s5_port', 0.3127264675087814),
 ('ppo_vol_port', 0.31391671831526435),
 ('unit_port', 0.3139167798238576),
 ('ppo_sharpe_port', 0.4062215466936162)]
