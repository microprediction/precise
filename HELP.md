You can help create Elo ratings as follows:

    git clone https://github.com/microprediction/precise.git
    cd precise
    pip install -e . 
    python3 precise/skatervaluation/battlescripts/manager_var/stocks\?topic=stocks\&n_dim=int:200\&n_obs=int:225\&n_burn=int:200\&k=int:1.py
    
This should start to populate a new file which you can PR 

