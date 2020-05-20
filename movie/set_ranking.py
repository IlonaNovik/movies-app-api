from core.models import Top


def set_rank_for_movie(comments):
    """Function for setting rank to movies"""

    movie_id_list = []

    for comment in comments:
        movie_id_list.append(
            comment.movie_id
        )

    counters = {i: movie_id_list.count(i) for i in movie_id_list}

    length = len(counters)
    result = []

    if length == 1:
        for key, value in counters.items():
            temp = Top.objects.create(
                movie_id=key, total_comments=value, rank=1
            )
            result.append(temp)

    elif length == 2:
        if len(counters.values()) != len(set(counters.values())):
            for key, value in counters.items():
                temp = Top.objects.create(
                    movie_id=key, total_comments=value, rank=1
                )
                result.append(temp)
        else:
            max_key = max(counters, key=counters.get)
            min_key = min(counters, key=counters.get)

            high = Top.objects.create(
                movie_id=max_key, total_comments=counters[max_key], rank=1
            )
            low = Top.objects.create(
                movie_id=min_key, total_comments=counters[min_key], rank=2
            )

            result.append(high)
            result.append(low)

    elif length > 2:
        all_values = counters.values()
        max_value = max(all_values)
        min_value = min(all_values)

        if max_value == min_value:
            for key, value in counters.items():
                temp = Top.objects.create(
                    movie_id=key, total_comments=value, rank=1
                )
                result.append(temp)
        else:
            for key, value in counters.items():

                if value == max_value:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=1
                    )
                    result.append(temp)

                elif value == min_value:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=3
                    )
                    result.append(temp)

                else:
                    temp = Top.objects.create(
                        movie_id=key, total_comments=value, rank=2
                    )
                    result.append(temp)

            counter = 0
            for item in result:
                if item.rank == 2:
                    counter += 1
            if counter == 0:
                for item in result:
                    if item.rank == 3:
                        item.rank = 2

    return result
