1、运行环境 arcgis 10.2  arcpy  python 2.7！！！！

2、数据准备：
	a、demo.py 同目录下 建立 data文件夹！ 里面存放 csv数据
	b、 把 csv数据 第二列 删除！ time(hr)         7.6000
	c、csv文件名不能出现 类似【point - 副本】 中文空格名
	
3、执行demo.py

4、结果文件存放在 result文件夹下，过程文件存放在 temp，每次运行会 清空 temp文件夹！

备注 ：

	克里金插值参数：
	半变异函数：CIRCULAR
	cellsie： 为默认值
	Radius：  Fixed
	
	等值线参数：
	高程字段：eta  // 代码对应字段可以做修改！
	等值线间距：3
	等值线起点：0 默认值
	
	
	
	