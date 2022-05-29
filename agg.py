import pandas as pd


def main():
    df = pd.read_csv("results.csv", parse_dates=["date"])
    new_df = df.groupby([pd.Grouper(key="date", freq="1D"), "url"]).last().copy()
    print(new_df)
    res = []
    agg_results = new_df.to_dict()["results"]
    for k, v in agg_results:
        temp = {}
        temp["url"] = v
        # temp["date"] = str(k.date())
        # temp["results"] = agg_results[(k, v)]
        temp[str(k.date())] = agg_results[(k, v)]
        res.append(temp)

    print(res)
    out_df = pd.DataFrame(res)
    out_df.fillna(0, inplace=True)

    cols = list(out_df.columns)[1:]
    res = out_df.groupby(["url"], as_index=False).agg({col: "sum" for col in cols})
    res.to_csv("agg_results.csv", index=False)


if __name__ == "__main__":
    main()
