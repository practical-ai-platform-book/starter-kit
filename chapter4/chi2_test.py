from scipy.stats import chi2_contingency


def main():
    data = [[1000, 9000], [1100, 8900]] # 各グループ1万サンプルあり、CVRが[10%, 11%]の場合のデータという想定
    x2, p, dof, expected = chi2_contingency(data, correction=False)
    print("p値", p)


if __name__ == "__main__":
    main()
