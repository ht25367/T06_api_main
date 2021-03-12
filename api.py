import requests
import urllib
from unicodedata import east_asian_width
import json
import csv

def get_zen_count(text):
	count=0
	for c in text:
		if east_asian_width(c) in "FWA":
			count +=1
	return count

def get_api(url):
	result = requests.get(url)
	return result.json()



def main():
	keyword = "鬼滅"
	url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={}&applicationId=1019079537947262807".format(keyword)

	# 検索結果の、商品名と価格
	print("検索ワード「鬼滅」\n１ページ目の商品名　： 価格")
	r = get_api(url)
	r = r["Items"]
	for r_data in r:
		name = r_data["Item"]["itemName"][:10]
		name += " " * (10-get_zen_count(name))
		print( f"{name}：{str(r_data['Item']['itemPrice']).rjust(5)}円")
	print("-----------------------------------\n\n")



	# 任意商品の、最安値と最高値
	keyword = "MacBook"
	url = f"https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&keyword={keyword}&minPrice=50000&maxPrice=1000000&applicationId=1019079537947262807"
	r = get_api(url)
	min_item = {"item":"","price":999999}
	max_item = {"item":"","price":0}

	for r_data in r["Products"]:
		if min_item["price"] > r_data["Product"]["minPrice"]:
			min_item["price"] = r_data["Product"]["minPrice"]
			min_item["item"] = r_data["Product"]["productName"]
		if max_item["price"] < r_data["Product"]["maxPrice"]:
			max_item["price"] = r_data["Product"]["maxPrice"]
			max_item["item"] = r_data["Product"]["productName"]
		print(f'{r_data["Product"]["productName"][:20]} 最安値：{r_data["Product"]["minPrice"]}、最高値：{r_data["Product"]["maxPrice"]}')
	print("\n検索ワードプロダクト「MACBook」\n検索結果１ページ目の、")
	print(f'最安値は、{min_item["item"]} の {min_item["price"]}円')
	print(f'最高値は、{max_item["item"]} の {max_item["price"]}円 です。')
	print("-----------------------------------\n\n")



	# 任意ジャンルの、ランキング一覧
	print("楽天「サービス・リフォーム」ランキング")
	elements = "rank,itemName,catchcopy"
	genre = "101438"
	page = "1"
	url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&applicationId=1019079537947262807&elements={elements}&genreId={genre}&page={page}"
	r = get_api(url)

	# csvファイルに書き込み
	with open("ranking.csv","w",encoding="utf_8",newline='') as f:
		writer = csv.DictWriter( f,r["Items"][0]["Item"].keys() )
		writer.writeheader()
		for r_data in r["Items"]:
			writer.writerow( r_data["Item"] )
		print("１ページ目を ranking.csv に出力しました。")


main()