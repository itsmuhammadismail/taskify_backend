import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommender(running_tasks, todo_tasks):
    todo_tasks.insert(0, running_tasks[0])
    running_tasks_df = pd.DataFrame(running_tasks)
    todo_tasks_df = pd.DataFrame(todo_tasks)

    # running_tasks_df = running_tasks_df[['id', 'desc']]
    # todo_tasks_df = todo_tasks_df[['id', 'desc']]

    cv = CountVectorizer(max_features=2500, stop_words='english')
    vector = cv.fit_transform(todo_tasks_df['desc']).toarray()

    similarity = cosine_similarity(vector)

    # print(similarity)
    # print(todo_tasks_df['desc']
    #       == running_tasks[0]['desc'])

    index = todo_tasks_df[todo_tasks_df['desc']
                          == running_tasks[0]['desc']].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_task_df = todo_tasks_df.iloc[distances[1][0]]
    recommended_tasks = recommended_task_df.to_dict()

    return recommended_tasks
