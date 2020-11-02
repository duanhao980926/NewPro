# 匹配名称的顺序后期需要持续优化
# 定义关键列、未能成功识别关键列会导致程序报错、退出、或跳过对当前文件的处理
# 1.02 20191006 把只针对销售数据的字段匹配清单扩展为覆盖进销存PSI数据
# 1.01 20190813把系统导出时使用的英文字段名加入自动匹配关系
# 1.00 初始状态

# 通用关键字段
productName = ['产品名称', '产品原始名称', '产品通用名', '药品通用名称', '产品名', '品名', '药品名称', '物料名称', '货品名称', '商品名称', '商品名',
              '货物名称', 'productName', 'MAKTX',
              '通用名(商品名)', '商品通用名', '通用名称', '通用名', '物料描述', '品名/规格/生产厂商', '存货名称', '药品通用名称(商品名)', '商品说明',
              '品种名称', '药品名/通用名', '品名/规格', '通用名/商品名称', '货品名称', '产品通用名称', '通用名', '品名-规格-产地', '产品商品名', '商品品名', '商品名及通用名',
              '货品通用名', '药品名', 'goodname', 'goodsName', 'spmch', '产品原始名', '商品', '药品通用名', 'prodname']
productCode = ['产品ID','产品代码', 'goodsOpcode', '商品编码', 'productCode', 'MATNR', 'prodcode']
productSpec = ['产品规格', 'productSpec', '商品规格/等级', '规格', '规格型号', '产品型号', '商品规格', '药品规格', '货品规格', '品种规格', '规格/型号', 'spec',
              'goodsDesc', 'shpgg', 'NORMT','specification','prodspec']
lotNo = ['批号', 'productLot', '生产批号', 'LOT', 'Batch', 'Lot', 'BATCH', 'lotnumber', '产品批号', 'goodsLotNo', 'LICHA', 'productBatch',
             'pihao','batchNumber','prodlotno']
expirationDateTitles = ['产品效期', '有效期', 'validitydate', '失效日期', 'goodsExpDate', 'sxrq', '失效效期', 'VFDAT']
qty = ['销售数量','数量', 'qty', '药品数量', '配送数量', '销售量', '出库数量', '出库量', '配送量', '订单数量', '基本单位数量', '出/入库数量', '销数量', 'excuteQty',
             '执行数量', '实际数量', ' 出库数', '开票数量', '数量[汇总]', '发出数', '发货数量', '使用单位数量', '单据数量', 'quantity', 'execQty', 'shl',
             '库存数量', '库存总数量', 'qtyOnhand', '采购数量', '产品数量', 'purchaseExecQty', 'FKIMG', 'MENGE','quantity','prodquan']
price = ['价格','含税单价', 'price', '单价', '销售单价', '零售价', '含税价', '不含税价', '折扣价', '无税单价', 'taxrate', 'dj', 'BUALT_DJ',
               '函数单价', 'prodprice']
salesDate = ['销售日期','销售时间', 'date', '销售出库日期', '配送日期', '日期', '时间', '开票日期', '出库日期', '业务时间', '记账日期', '业务日期', '释放日期',
               '金税日期', '记帐日期', '过账日期', '开单日期', '生效日期', '生效时间', '凭证日期', '单据日期', '创建日期', '业务账时间', '流向时间', '流向日期', '开票时间',
               '开单时间', '制单日期', '销售/退回日期', '记账曰期', '流向日期', '记保管帐日期', '记保管账日期', '配货时间', 'FKDAT', 'saleDate',
               '订单日期', 'orderdate', 'dateInvprint', 'rq', '出库时间', '库存日期', 'today', '采购日期', 'dateFetch', '入库日期','sellDate','createdate']
purchaseDate = ['入库日期', '采购日期', 'dateFetch', '入库日期', '日期', 'date', 'data', 'BUDAT', 'createDate','buyDate','billdate']
inventoryDate = ['库存时间', 'date', 'dateInvprint', 'rq', '库存日期','storageDate', 'inventoryReportDate', 'BUDAT', '直连时间', 'stockdate']
inventoryStatus = ['库存状态', 'status']
customerName = ['客户名称', 'customerName', '门店名称', '门店', '销售客户名称', '机构名称', '客商名称', '目标业务机构', '买方', '客户', '往来单位名称', '往来单位',
              '售达方描述', '相关单位名称', '调入货位名', '调入货位', '业务机构名称', '单位名称', '单位全名', '客户描述', '商品去向', '业务部门', '相关明细', 'CSTNM',
              '销往单位', '采购方名称', '客商', '客户简称', '货位名称', '客户名', '销售客户', '客户原始名称', '购货单位名称', '配送对象', '医院名称', '对方单位', '对方名称',
              '业务单位名称', '调入分店名称', 'client', 'clientName', 'dwmch', 'custname']
customerCode = ['客户ID','客户代码', 'customerCode']
customerProvince = ['客户城市', 'customerProvince']
addressTitles = ['送货地址', 'customerAddress', '地址', '配送地址', '客户地址', 'addressName', '门店地址', 'DIZHI']
# subsidiaryMarkTitles = ['分公司名称', 'subsidiaryMark', '分公司标识', '销售方代码', '经销商名称', '采购方代码', '公司代码']
subsidiaryMarkTitles = ['分公司名称', '分公司标识', '销售方代码', '采购方代码', '公司代码', '销售方名称','branchOrgName','purname','ownername']
supplierName = ['供应商名称', '供应商原始名称', 'salesName', 'clientName', 'dwmch', 'supplierName', '供货单位', '供应商', '销售方名称', 'NAME1', 'supname']
supplierCode = ['供应商代码', '公司代码', '销售方代码', 'LIFNR']
supplierProvince = ['供应商城市']
branchCode = ['分公司ID','分公司代码', '经销商代码']
branchProvince = ['分公司城市']
salesNum = ['销售单据号','销售单号', '经销商发货单号', '单据编号', '单据号', 'VBELN']
purchaseNum = ['入库单号', '单据编号', '单据号']
amount = ['金额（含税）', 'amount', '金额', '总金额', '销售金额', '含税金额', '不含税金额', '折扣金额', 'je', '价税合计', 'BUALT_JE', 'prodamount']
productOrigin = ['生产厂家', 'productOrigin', 'manufacture', '生产厂商描述', '生产企业名称', '生产企业', '厂家', '生产商', '生产厂商', '产地', '厂商', '产家', '货品厂地',
                     'producer', '厂牌', '生产厂商简称', '供应商', 'restrictioncompany', 'shpchd', '厂家名称', 'NAME1_SC','factory','factory','prodproducer']


# 定义可选列、后续如未识别到、做记录和提示、但不影响流程进行
# 通用可选字段
# unitTitles = ['单位', 'unit', '包装单位', '销售单位', '产品单位', 'packageunit', 'goodsUnit', 'dw']

# 销售可选列
# saleTypeTitles = ['saleType', '出货类型', '单据类型', 'saleType', 'zhy', '销售类型']
# expdateTitles = ['expdate', '保质期', '有效期至', '有效期', '到期日期', '到期日', '质保期']  # 保质期

# 采购可选列
# supplierNameTitles = ['supplierName', '供应商原始名称', 'salesName', '供应商名称', '供货商名称', 'clientName', 'dwmch', '供货单位','供应商']
# productOriginTitlesP = ['productOrigin', '生产厂家', 'salesName', 'productName', 'shpchd', '产地', '生产厂商', '厂家名称']

# 库存关键列
# inventoryReportDateTitlesI = ['inventoryReportDate', '库存日期', 'orderdate', 'today', '库存时间']
# 库存可选列
# supplierNameTitlesI = ['supplierName', '供应商名称', '供应商代码', '公司名称']
manufactureDateTitlesI = ['生产日期', 'manufactureDate', 'manufacturedate', 'goodsProdDate', 'baozhiqi', 'HSDAT']
# stockStateTitlesI = ['stockState', '库存状态', 'taxamount']
# entryDateTitlesI = ['entryDate', '库存日期', 'orderdate', '入库时间', '创建时间']
# productLotTitlesI = ['productLot', '批号', 'lotnumber', '产品批号', 'goodsLotNo', 'pihao']
# manufactureTitlesI = ['manufacture', '生产厂家', 'restrictioncompany', 'shpchd', '厂家名称', '生产厂商']


# s_namelist = [productName, productCode, productSpec, lotNo, expirationDateTitles, qty, price, salesDate, customerName, customerCode, customerProvince, addressTitles, subsidiaryMarkTitles, branchCode, branchProvince, salesNum, amount, productOrigin]
s_namelist = [productName, productCode, productSpec, lotNo, expirationDateTitles, qty, price, salesDate, customerName,customerCode,customerProvince, addressTitles, subsidiaryMarkTitles,branchCode,branchProvince,salesNum]

p_namelist = [productName, productCode, productSpec, lotNo, expirationDateTitles, qty, price, purchaseDate, supplierName, supplierCode, supplierProvince, purchaseNum, amount, productOrigin]

i_namelist = [productName, productCode, productSpec, lotNo, expirationDateTitles, qty, inventoryDate, inventoryStatus, productOrigin, subsidiaryMarkTitles, branchCode, branchProvince]
