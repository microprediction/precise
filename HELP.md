You can help create Elo ratings as follows:

    git clone https://github.com/microprediction/precise.git
    cd precise
    pip install -e . 
    python3 precise/skatervaluation/battlescripts/manager_var/stocks\?topic=stocks\&n_dim=int:500\&n_obs=int:225\&n_burn=int:200\&k=int:5.py
    
This should start to populate a new file which you can PR. It will go in [here](https://github.com/microprediction/precise/tree/main/precise/skatervaluation/battleresults/manager_var/stocks_5_days_p500_n200) 

