# 数据集说明
豆瓣项目的数据集为sql格式，里面共有两个表，movie和user。请使用mysql进行读取和操作，以避免出现不必要的麻烦，推荐安装好mysql后使用SQLyog图形管理工具直接导入。

## movie表
	- number：该数据集中电影的编号，从1到1000
	- rate：电影在豆瓣的平均分
	- title：电影名字
	- url：电影链接
	- id：电影在豆瓣中的编号
	- directors：电影的导演
	- year：电影首播年份
	- actors：主演
	- type：电影类型
	- countries：制片国家、地区
	- summary：电影剧情简介

## user表
	- user_id：该数据集中用户的编号，从1到1000
	- name：用户在豆瓣中的编号
	- rates：用户看过的所有电影编号以及该用户给出的评分
	- following_id：该用户关注的所有用户的编号
	- comments：该用户对看过的一些电影的部分评论

## 其他
此外我们把用pandas读取的两个表直接存到了pickle里面便于读取。
