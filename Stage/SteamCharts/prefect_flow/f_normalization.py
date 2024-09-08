import time
import datetime 
import pandas as pd
from prefect import flow, task


@flow(name="test")
def normalization():
    today = datetime.datetime.now()
    date = today.strftime('%Y-%m-%d %H:%M')
    _today = today.strftime('%m-%d')
    df = pd.read_csv(f'test({_today}).csv')
    df = df.drop('Rank', axis=1)
    df = df.drop('Name', axis=1)
    df = df.drop('Current_Players', axis=1)
    df = df.drop('Peak_Players', axis=1)

    df.to_csv(f'test({_today})_normalization.csv', encoding='utf-8', index=False)



if __name__ == "__main__":
    from prefect_github import GitHubRepository

    # normalization.serve(name="develop")
    normalization.from_source(
        source=GitHubRepository.load("steam_trend"),
        entrypoint="f_normalization.py:normalization",
    ).deploy(
        name="test-normalization",
        tags=["test", "project_1"],
        work_pool_name="docker",
        job_variables=dict(pull_policy="Never"),
        # parameters=dict(name="Marvin"),
        cron="5 12 * * *"
    )

    


