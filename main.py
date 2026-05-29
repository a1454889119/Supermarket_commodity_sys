# -*- coding:utf-8 -*-
import sys
import cv2
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QRegExp, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QTextCursor, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox,QWidget,QTableWidgetItem,QSlider,QGridLayout
from PyQt5.uic import loadUi
import anniu
import time
import re
import torch
import pathlib
import pandas as pd
from PyQt5 import QtCore
from PIL import Image
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# 图片转换
def convert2QImage(img):
    h, w, c = img.shape
    return QImage(img, w, h, w * c, QImage.Format_RGB888)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('./images/jieshuan_1920_1080.ui', self)
        self.setWindowIcon(QIcon('./icons/gouwu.png'))
        self.model = torch.hub.load(".", "custom",path='.//weight_file//weight_x.pt',device='0',source='local')
        self.video = cv2.VideoCapture()
        self.video_kaiguan=False
        self.shishi_shangping_dic={}
        self.parameters={'Conf':0.6,'Iou':0.45}
        self.shangping_jiage={'上好佳荷兰豆55g': 4.5,'菜园小饼80g': 2.8,'上好佳鲜虾片40g': 5.0,'上好佳蟹味逸族40g': 4.8,'妙脆角魔力炭烧味65g': 5.5,'盼盼烧烤牛排味块105g': 6.0,'上好佳鲜虾条40g': 5.0,'上好佳洋葱圈40g': 4.5,'上好佳日式鱼果海苔味50g': 5.2,'奇多日式牛排味90g': 5.8,'奇多美式火鸡味90g': 5.8,'上好佳粟米条草莓味40g': 4.2,'甘源蟹黄味瓜子仁75g': 8.5,'惠宜开心果140g': 12.0,'惠宜咸味花生350g': 9.9,'惠宜腰果160g': 18.0,'惠宜枸杞100g': 26.0,'惠宜地瓜干228g': 12.5,'惠宜泰国芒果干80g': 9.0,'惠宜黄桃果干75g': 9.5,'惠宜柠檬片65g': 8.0,'新疆和田滩枣454g': 25.0,'惠宜香菇100g': 6.5,'惠宜桂圆干500g': 38.0,'惠宜茶树菇200g': 12.0,'豪雄单片黑木耳150g': 7.5,'惠宜煮花生454g': 18.0,'惠宜黄花菜100g': 5.0,'洽洽凉茶瓜子150g': 6.8,'洽洽奶香味瓜子150g': 6.8,'车仔茶包绿茶50g': 8.0,'车仔茶包红茶50g': 8.0,'优乐美香芋味80g': 3.5,'优乐美红豆奶茶65g': 3.0,'欢泥冲调土豆粥25g': 4.5,'江中猴姑早餐米稀40g': 5.0,'永和豆浆甜豆浆粉210g': 4.8,'立顿柠檬风味茶180g': 12.0,'桂格多种莓果麦片40g': 4.2,'荣怡谷麦加黑米味30g': 2.5,'荣怡谷麦加红豆味30g': 2.5,'今野香辣牛肉面112g': 4.8,'今野老坛酸菜牛肉面118g': 5.0,'今野红烧牛肉面114g': 4.8,'合味道海鲜风味84g': 3.8,'康师傅白胡椒肉骨面76g': 4.0,'康师傅香辣牛肉面105g': 4.5,'康师傅香辣蒜味排骨面108g': 4.8,'康师傅藤椒牛肉面82g': 4.2,'华丰鸡肉三鲜伊面87g': 4.0,'康师傅黑胡椒牛排面104g': 4.5,'五谷道场红烧牛肉面100g': 4.2,'康师傅老坛酸菜牛肉面114g': 5.0,'Aji泡芙饼干芒果菠萝味60g': 6.5,'庆联蓝莓味夹心饼63g': 5.8,'庆联凤梨味夹心饼63g': 5.8,'庆联草莓味夹心饼63g': 5.8,'嘉顿威化饼干草莓味50g': 3.5,'嘉顿威化饼干柠檬味50g': 3.5,'爱时乐香草牛奶味50g': 3.0,'爱时乐巧克力味50g': 3.0,'百力滋海苔味60g': 4.5,'百力滋草莓牛奶味45g': 4.0,'雀巢脆脆鲨80g': 6.0,'纳宝帝巧克力味威化58g': 5.0,'桂力地中海风味面包条50g': 4.5,'康师傅妙芙巧克力味48g': 5.0,'爱乡亲唱片面包90g': 3.5,'达利园派草莓味单个装*': 5.0,'mini奥利奥55g': 6.5,'农夫山泉矿泉水550ml': 1.5,'怡宝矿泉水555ml': 1.5,'可口可乐零度500ml': 3.0,'可口可乐500ml': 3.0,'百事可乐600ml': 3.5,'芬达苹果味500ml': 3.0,'芬达橙味500ml': 3.0,'雪碧500ml': 3.0,'喜力啤酒500ml': 3.5,'百威啤酒600ml': 3.8,'百事可乐330ml': 2.0,'可口可乐330ml': 2.0,'王老吉310ml': 3.5,'茶派柚子绿茶500ml': 4.0,'茶派玫瑰荔枝红茶500ml': 4.0,'康师傅冰红茶250ml': 2.5,'加多宝250ml': 3.0,'RIO果酒水蜜桃味275ml': 6.0,'RIO果酒蓝玫瑰威士忌味275ml': 6.0,'牛栏山二锅头100ml': 3.5,'哈尔滨啤酒330ml': 3.0,'青岛啤酒330ml': 3.0,'雪花啤酒330ml': 3.0,'哈尔滨啤酒500ml': 4.0, 'KELER啤酒500ml': 3.5,'百威啤酒500ml': 3.8,'QQ星全聪奶125ml': 2.8,'QQ星均膳奶125ml': 2.8,'娃哈哈AD钙奶220g': 3.5,'活力宝动力源105ml': 2.0,'旺仔牛奶复原乳250ml': 3.2,'伊利纯牛奶250ml': 3.5,'维他低糖原味豆奶250ml': 3.0,'百怡花生牛奶250ml': 3.8,'惠宜原味豆奶250ml': 2.5,'伊利优酸乳250ml': 3.2,'伊利早餐奶250ml': 3.5,'达利园桂圆莲子360g': 25.0,'银鹭冰糖百合银耳280g': 12.5,'喜多多什锦椰果567g': 35.0,'都乐菠萝块567g': 18.0,'都乐菠萝块234g': 9.5, '银鹭薏仁红豆粥280g': 8.5,'银鹭莲子玉米粥280g': 8.5,'银鹭紫薯紫米粥280g': 8.5,'银鹭椰奶燕麦粥280g': 8.5,'银鹭黑糖桂圆280g': 16.0,'梅林午餐肉340g': 9.8,'珠江桥牌豆豉鱼150g': 9.0,'古龙原味黄花鱼120g': 12.0,'雄鸡标椰浆140ml': 4.5,'德芙芒果酸奶巧克力42g': 6.5,'德芙摩卡巴旦木巧克力43g': 6.5,'德芙百香果白巧克力42g': 6.5,'MM花生牛奶巧克力豆40g': 5.0,'MM牛奶巧克力豆40g': 5.0,'好时牛奶巧克力40g': 4.0,'好时曲奇奶香白巧克力40g': 4.0,'脆香米海苔白巧克力24g': 3.5,'脆香米奶香白巧克力24g': 3.5,'士力架花生夹心巧克力51g': 5.5,'士力架燕麦花生夹心巧克力40g': 4.5,'士力架辣花生夹心巧克力40g': 4.5,'炫迈果味浪薄荷味37g': 9.5,'炫迈果味浪柠檬味37g': 9.5,'炫迈薄荷味21g': 9.0,'炫迈葡萄味21g': 9.0,'炫迈西瓜味21g': 9.0,'炫迈葡萄味50g': 9.0,'绿箭无糖薄荷糖茉莉花茶味34g': 12.0,'绿箭5片装15g': 2.5,'比巴卜棉花泡泡糖可乐味11g': 1.5,'比巴卜棉花泡泡堂葡萄味11g': 1.5,'星爆缤纷原果味25g': 1.5,'阿尔卑斯焦香牛奶味硬糖45g': 4.0,'阿尔卑斯牛奶软糖黄桃酸奶味47g': 4.5,'阿尔卑斯牛奶软糖蓝莓酸奶味47g': 4.5,'王老吉润喉糖28g': 3.8,'伊利牛奶片蓝莓味32g': 3.5,'熊博士口嚼糖草莓牛奶味52g': 4.5,'彩虹糖原果味45g': 2.5,'宝鼎天鱼陈酿米醋245ml': 4.0,'恒顺香醋340ml': 2.8,'太太乐鸡精200g': 5.5,'家乐香菇鸡茸汤料41g': 3.0,'惠宜辣椒粉15g': 1.2,'惠宜生姜粉15g': 1.2,'味好美椒盐20g': 1.5,'海星加碘精制盐400g': 2.0,'恒顺料酒500ml': 6.5,'东古味极鲜酱油150ml': 3.5,'东古一品鲜酱油150ml': 3.2,'欣和六月鲜酱油160ml': 3.8,'李施德林零度漱口水80ml': 9.5,'舒肤佳纯白清香沐浴露100ml': 6.0,'美涛定型啫喱水60ml': 9.0,'清扬男士洗发露活力运动薄荷型50ml': 6.5,'蓝月亮风清白兰洗衣液80g': 1.8,'高露洁亮白小苏打180g': 6.5,'高露洁冰爽180g': 6.5,'舒克宝贝儿童牙刷': 4.0,'云南白药牙膏45g': 6.5,'舒亮皓齿白80g': 9.5,'清风原木纯品金装100x3': 8.9,'洁柔face150x3': 9.9,'斑布100x3': 5.9, '维达婴儿150x3': 9.9,'相印小黄人150x3': 9.9,'清风原木纯品黑耀150x3': 14.9,'洁云绒触感130x3': 9.9,'舒洁萌印花120x2': 6.9,'相印红悦130x3': 9.9,'得宝苹果木味90x4': 9.9,'清风新韧纯品130x3': 11.9,'金鱼竹浆绿135x3': 11.9,'清风原木纯品150x2': 9.9,'洁柔face130x3': 8.9,'维达立体美110x3': 7.9,'洁柔CS单包*': 1.0,'相印小黄人单包*': 1.0,'清风原色单包*': 1.0,'相印茶语单包*': 1.0,'清风质感纯品单包*': 1.2,'米奇1928笔记本': 8.0,'广博固体胶15g': 2.5,'票据文件袋': 1.5,'晨光蜗牛改正带': 3.0,'鸿泰液体胶50g': 4.0,'马培德自粘性标签': 2.0,'东亚记号笔': 2.5}
        self.Thread_video_pred=False
        self.shangping={'shanghaojia helandou 55g': '上好佳荷兰豆55g', 'caiyuanxiaobing 80g': '菜园小饼80g', 'shanghaojia xianxiapian 40g': '上好佳鲜虾片40g', 'shanghaojia xiewei 40g': '上好佳蟹味逸族40g', 'miaocuijiao tankaowei 65g': '妙脆角魔力炭烧味65g', 'panpanshaokao niupai 105g': '盼盼烧烤牛排味块105g', 'shanghaojia xianxiatiao 40g': '上好佳鲜虾条40g', 'shanghaojia yangchonquan 40g': '上好佳洋葱圈40g','shanghaojia rishi haitai 50g': '上好佳日式鱼果海苔味50g', 'qiduorisi niupaiwei 90g': '奇多日式牛排味90g', 'qiduomeishi huojiwei 90g': '奇多美式火鸡味90g', 'shanghaojia caomeiwei 40g': '上好佳粟米条草莓味40g', 'ganquan xiehuang guaziren 75g': '甘源蟹黄味瓜子仁75g', 'huiyi kaixingguo140g': '惠宜开心果140g', 'huiyi xianweihuasheng 350g': '惠宜咸味花生350g', 'huiyi yaoguo 160g': '惠宜腰果160g', 'huiyi gouqi 100g': '惠宜枸杞100g', 'huiyi diguagan 228g': '惠宜地瓜干228g', 'huiyi taiguomangguo 80g': '惠宜泰国芒果干80g', 'huiyi huangtaoguogan 75g': '惠宜黄桃果干75g', 'huiyi lingmengpian 65g': '惠宜柠檬片65g', 'xingjianghetianganzhao 454g': '新疆和田滩枣454g', 'huiyi xiangguo 100g': '惠宜香菇100g', 'huiyi guiyuangan 500g': '惠宜桂圆干500g', 'huiyi chashugu 200g': '惠宜茶树菇200g', 'haoxion heimuer 150g': '豪雄单片黑木耳150g', 'huiyi zhuhuasheng 454g': '惠宜煮花生454g', 'huiyi huanghuacai 100g': '惠宜黄花菜100g', 'qiaqia liangchaguazi 150g': '洽洽凉茶瓜子150g', 'qiaqia naixiangguazi 150g': '洽洽奶香味瓜子150g', 'chezaichabao lvcha 50g': '车仔茶包绿茶50g', 'chezaichabao honcha 50g': '车仔茶包红茶50g', 'youlemei xiangyu 80g': '优乐美香芋味80g', 'youlemei hondou 65g': '优乐美红豆奶茶65g', 'huanni tudouzhou 25g': '欢泥冲调土豆粥25g', 'jiangzhonhougu 40g': '江中猴姑早餐米稀40g', 'yonhedoujiangtiandou 210g': '永和豆浆甜豆浆粉210g', 'lidunningmengcha 180g': '立顿柠檬风味茶180g', 'guige maipian 40g': '桂格多种莓果麦片40g', 'ronyi heimiwei 30g': '荣怡谷麦加黑米味30g', 'ronyi hondouwei 30g': '荣怡谷麦加红豆味30g', 'jinye xianglaniurou 112g': '今野香辣牛肉面112g', 'jinye laotanshuancai 118g': '今野老坛酸菜牛肉面118g', 'jinye honshaoniurou 114g': '今野红烧牛肉面114g', 'heweidao haixian 84g': '合味道海鲜风味84g', 'kangsifu baihujiaorougu 76g': '康师傅白胡椒肉骨面76g', 'kangsifu xianglaniurou 105g': '康师傅香辣牛肉面105g', 'kangsifu xianglashuanwei 108g': '康师傅香辣蒜味排骨面108g', 'kangsifu tenjiaoniurou 82g': '康师傅藤椒牛肉面82g', 'huafengjiroumian87g': '华丰鸡肉三鲜伊面87g', 'kangsifu heihujiaoniupai 104g': '康师傅黑胡椒牛排面104g', 'wugudaochang honshao 100g': '五谷道场红烧牛肉面100g', 'kangsifu laotanshuancai 114g': '康师傅老坛酸菜牛肉面114g', 'Ajipaofu maoguobolo 60g': 'Aji泡芙饼干芒果菠萝味60g', 'qinlian lanmei 63g': '庆联蓝莓味夹心饼63g', 'qinlian fengli 63g': '庆联凤梨味夹心饼63g', 'qinlian caomei 63g': '庆联草莓味夹心饼63g', 'jiadunweihua caomei 50g': '嘉顿威化饼干草莓味50g', 'jiadunweihua ningmeng 50g': '嘉顿威化饼干柠檬味50g', 'aishile caoxiangniunai 50g': '爱时乐香草牛奶味50g', 'aishile qiaokeli 50g': '爱时乐巧克力味50g', 'bailichi haitaiwei 60g': '百力滋海苔味60g', 'bailichi caomeiniunai 45g': '百力滋草莓牛奶味45g', 'qiechaocuicuisha 80g': '雀巢脆脆鲨80g', 'nabaodi qiaokeli 58g': '纳宝帝巧克力味威化58g', 'guilidizhonhai 50g': '桂力地中海风味面包条50g','kangshifumiaofu qiaokeli 48g': '康师傅妙芙巧克力味48g', 'aixiangqingchangpian 90g': '爱乡亲唱片面包90g', 'daliyuanpai caomeiwei': '达利园派草莓味单个装*','mini aoliao 55g': 'mini奥利奥55g', 'nonfusanquan 550ml': '农夫山泉矿泉水550ml', 'yibao 555ml': '怡宝矿泉水555ml', 'kekoukele 0 500ml': '可口可乐零度500ml', 'kekoukele 500ml': '可口可乐500ml', 'baisikele 600ml': '百事可乐600ml', 'fenda pingguo 500ml': '芬达苹果味500ml', 'fenda chengzhi 500ml': '芬达橙味500ml', 'quebi 500ml': '雪碧500ml', 'xili piqiu 500ml': '喜力啤酒500ml', 'baiwei pijiu 600ml': '百威啤酒600ml', 'baisikele 330ml': '百事可乐330ml', 'kekoukele 330ml': '可口可乐330ml', 'wanglaoji 310ml': '王老吉310ml', 'capai youzhilvcha 500ml': '茶派柚子绿茶500ml', 'capai meiguilizhi honcha 500ml': '茶派玫瑰荔枝红茶500ml', 'kangshifu binghoncha 250ml': '康师傅冰红茶250ml', 'jiaduobao 250ml': '加多宝250ml', 'RIOguojiu suimitao 275ml': 'RIO果酒水蜜桃味275ml', 'RIOguojiu lanmeigui 275ml': 'RIO果酒蓝玫瑰威士忌味275ml', 'niulanshan erguotou 100ml': '牛栏山二锅头100ml', 'haerbing pijiu 330ml': '哈尔滨啤酒330ml', 'qingdao pijiu 330ml': '青岛啤酒330ml', 'xuehua pijiu 330ml': '雪花啤酒330ml', 'haerbing pijiu 500ml': '哈尔滨啤酒500ml', 'KELERpijiu 500ml': 'KELER啤酒500ml', 'baiwei pijiu 500ml': '百威啤酒500ml', 'QQxingquanchonnai 125ml': 'QQ星全聪奶125ml', 'QQxingjunshannai 125ml': 'QQ星均膳奶125ml', 'wahaha AD 220g': '娃哈哈AD钙奶220g', 'huolibaodonliyuan 105ml': '活力宝动力源105ml', 'wangzainiunai 250ml': '旺仔牛奶复原乳250ml', 'yilichunniunai 250ml': '伊利纯牛奶250ml', 'weita dounai 250ml': '维他低糖原味豆奶250ml', 'baiyi huashengniunai 250ml': '百怡花生牛奶250ml', 'huiyi dounai 250ml': '惠宜原味豆奶250ml', 'yili youshuannu 250ml': '伊利优酸乳250ml', 'yili zaocannai 250ml': '伊利早餐奶250ml', 'daliyuan guiyuanlianzhi 360g': '达利园桂圆莲子360g', 'yinglu bintangbaiheyinger 280g': '银鹭冰糖百合银耳280g', 'xiduoduo yeguo 567g': '喜多多什锦椰果567g', 'doule boluo 567g': '都乐菠萝块567g', 'doule boluo 234g': '都乐菠萝块234g', 'yinglu hondou 280g': '银鹭薏仁红豆粥280g', 'yinglu yumi 280g': '银鹭莲子玉米粥280g', 'yinglu zhimi 280g': '银鹭紫薯紫米粥280g', 'yinglu yanmai 280g': '银鹭椰奶燕麦粥280g', 'yinglu heitang 280g': '银鹭黑糖桂圆280g', 'meiling wuchanrou 340g': '梅林午餐肉340g', 'zhujiangqiaopai 150g': '珠江桥牌豆豉鱼150g', 'gulon guihuayu 120g': '古龙原味黄花鱼120g', 'xiongjibiao 140ml': '雄鸡标椰浆140ml', 'defu maoguoshuannai 42g': '德芙芒果酸奶巧克力42g', 'defu badanmu 43g': '德芙摩卡巴旦木巧克力43g', 'defu baixiangguo 42g': '德芙百香果白巧克力42g', 'MMhuasheng niunai 40g': 'MM花生牛奶巧克力豆40g', 'MMniunai 40g': 'MM牛奶巧克力豆40g', 'haoshi niunai 40g': '好时牛奶巧克力40g', 'haoshi quxinaixiang 40g': '好时曲奇奶香白巧克力40g', 'chuixiangmi haitaibai 24g': '脆香米海苔白巧克力24g', 'chuixiangmi naixiangbai 24g': '脆香米奶香白巧克力24g', 'shilijia huasheng 51g': '士力架花生夹心巧克力51g', 'shilijia yanmai 40g': '士力架燕麦花生夹心巧克力40g', 'shilijia lahuasheng 40g': '士力架辣花生夹心巧克力40g', 'xuanmai bohewei 37g': '炫迈果味浪薄荷味37g', 'xuanmai ningmengwei37g': '炫迈果味浪柠檬味37g', 'xuanmai bohewei 21g': '炫迈薄荷味21g', 'xuanmai pitaowei 21g': '炫迈葡萄味21g', 'xuanmai xiguawei 21g': '炫迈西瓜味21g', 'xuanmai putaowei 50g': '炫迈葡萄味50g', 'lvjian pohemolihua 34g': '绿箭无糖薄荷糖茉莉花茶味34g', 'lvjian 5pian 15g': '绿箭5片装15g', 'bibabu kelewei 11g': '比巴卜棉花泡泡糖可乐味11g', 'bibabu putaowei 11g': '比巴卜棉花泡泡堂葡萄味11g', 'xinbaobingfen 25g': '星爆缤纷原果味25g', 'aerfeisi jiaoxiang 45g': '阿尔卑斯焦香牛奶味硬糖45g', 'aerfeisi huangtao 47g': '阿尔卑斯牛奶软糖黄桃酸奶味47g', 'aerfeisi nanmei 47g': '阿尔卑斯牛奶软糖蓝莓酸奶味47g', 'wanglaoji runhoutang 28g': '王老吉润喉糖28g', 'yili lanmeiwei niunaipian32g': '伊利牛奶片蓝莓味32g', 'xionbosi caomei 52g': '熊博士口嚼糖草莓牛奶味52g', 'caihontang 45g': '彩虹糖原果味45g', 'baodingtian chu 245ml': '宝鼎天鱼陈酿米醋245ml', 'henshunchu 340ml': '恒顺香醋340ml', 'taitaile jijing 200g': '太太乐鸡精200g', 'jialexiangguji 41g': '家乐香菇鸡茸汤料41g', 'huiyi lajiaofen 15g': '惠宜辣椒粉15g', 'huiyishengjiangfen 15g': '惠宜生姜粉15g', 'weihaomeijjiaoyan 20g': '味好美椒盐20g', 'haixing 400g': '海星加碘精制盐400g', 'henshunliaojiu 500ml': '恒顺料酒500ml', 'donguwei jiangyou 150ml': '东古味极鲜酱油150ml', 'donguoyiping jiangyou 150ml': '东古一品鲜酱油150ml', 'xingheliuyue jiangyou 160ml': '欣和六月鲜酱油160ml', 'lishide shukousui 80ml': '李施德林零度漱口水80ml', 'shufujia muyulu 100ml': '舒肤佳纯白清香沐浴露100ml', 'meitao 60ml': '美涛定型啫喱水60ml', 'qingyang 50ml': '清扬男士洗发露活力运动薄荷型50ml', 'lanyueliang 80g': '蓝月亮风清白兰洗衣液80g', 'gaolujie xiaoshuda 180g': '高露洁亮白小苏打180g', 'gaolujiebai binshuang 180g': '高露洁冰爽180g', 'shuliang yagao 80g': '舒亮皓齿白80g', 'yunlanbaiyao yagao 45g': '云南白药牙膏45g', 'shukebaobei ': '舒克宝贝儿童牙刷', 'qinfengyuanmu 100x3': '清风原木纯品金装100x3', 'jierou face 150x3': '洁柔face150x3', 'banbu 100x3': '斑布100x3', 'weidayinger 150x3': '维达婴儿150x3', 'xiangying 150x3': '相印小黄人150x3', 'qingfengyuanmu heiyao 150x3': '清风原木纯品黑耀150x3', 'jieyun 130x3': '洁云绒触感130x3', 'shujiemeng 120x2': '舒洁萌印花120x2', 'xiangying honyue 130x3': '相印红悦130x3', 'debao pingguo 90x4': '得宝苹果木味90x4', 'qingfeng xing 130x3': '清风新韧纯品130x3', 'jinyu zhujiang 135x3': '金鱼竹浆绿135x3', 'qinfengyuanmu 150x2': '清风原木纯品150x2', 'jierou face 130x3': '洁柔face130x3', 'weida litimei 110x3': '维达立体美110x3', 'jierouCS': '洁柔CS单包*', 'xiangyingxiaohuangren': '相印小黄人单包*', 'qinfengyuanshe danbao': '清风原色单包*', 'xiangying danbao': '相印茶语单包*', 'qingfengzhigan danbao': '清风质感纯品单包*','miqi1928': '米奇1928笔记本', 'guangbo gutijiao 15g': '广博固体胶15g', 'biaoju wenjudai': '票据文件袋', 'chengguang gaizhengdai ': '晨光蜗牛改正带', 'hontai 50g': '鸿泰液体胶50g', 'mapeide biaoqian': '马培德自粘性标签', 'donya jihaobi': '东亚记号笔'}
        self.startjieshuanButton.clicked.connect(self.video_pred)
        self.startjieshuanButton_2.clicked.connect(self.guanliyuan)
        self.jiesuan.clicked.connect(self.jiesuan1)
        self.move(0,0)

    def video_pred(self):
        self.video_kaiguan=True
        if self.Thread_video_pred==False:
            self.thread_1 = Thread()  # 创建线程
            self.thread_1.start()  # 开始线程

            self.thread_2=Thread_1()
            self.thread_2.start()  # 开始线程

    def guanliyuan(self):
        window_guanli.show()

    def jiesuan1(self):
        if self.video_kaiguan:
            if self.shishi_shangping_dic!={}:
                dic=self.shishi_shangping_dic
                df=pd.read_csv('xiaoshou.csv',index_col=0)
                for i in dic:
                    df.loc[i,:]=df.loc[i,:]+dic[i]
                df.to_csv('xiaoshou.csv')
            self.jiesuanlabel.setText('购买成功!')
            self.shishi_shangping_dic={}
            self.thread_jiesuan=Thread_jiesuan()
            self.thread_jiesuan.start()

class Thread(QThread):  # 视频检测
    def __init__(self):
        super().__init__()

    def run(self):
        window.video.open(0)  #http://admin:admin@192.168.1.41:8081
        while window.video_kaiguan:
            ret, frame = window.video.read()
            if not ret:
                window.timer.stop()  # 没有检测到视频，计时器停止
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                window.model.conf=window.parameters['Conf']
                window.model.iou=window.parameters['Iou']
                results = window.model(frame)
                if window.shishi_shangping_dic=={}:
                    for i in results.pred[0]:
                        window.shishi_shangping_dic[results.names[int(i[5])]] = window.shishi_shangping_dic.get(results.names[int(i[5])], 0) + 1
                image = results.render()[0]  # 推理结果，是个数组
                window.realTimeCaptureLabel.setPixmap(QPixmap.fromImage(convert2QImage(image)))  # 将图片显示到可视y化窗口的输出部分
                window.realTimeCaptureLabel.setScaledContents(True)
        else:
            window.realTimeCaptureLabel.clear()
            window.video.release()

class Thread_1(QThread):  # 表格更新
    def __init__(self):
        super().__init__()

    def run(self):
        while window.video_kaiguan:
            dic=window.shishi_shangping_dic
            dic1 = sorted(dic.items(), key=lambda d: d[0])
            dic = {}
            for i in dic1:
                dic[i[0]] = i[1]
            shangping = list(dic)
            sum=0
            for i in range(len(dic)):
                name = QTableWidgetItem(window.shangping[shangping[i]])
                counts = QTableWidgetItem(str(dic[shangping[i]]))
                sum1=dic[shangping[i]] * window.shangping_jiage[window.shangping[shangping[i]]]
                value = QTableWidgetItem(str(sum1))
                sum=sum+sum1
                window.tableWidget_1.setItem(i, 0, name)
                window.tableWidget_1.setItem(i, 1, counts)
                window.tableWidget_1.setItem(i, 2, value)
            value_sum_name=QTableWidgetItem('总价')
            window.tableWidget_1.setItem(len(dic), 0, value_sum_name)
            none = QTableWidgetItem('')
            window.tableWidget_1.setItem(len(dic), 1, none)
            value_sum = QTableWidgetItem(str(sum))
            window.tableWidget_1.setItem(len(dic), 2, value_sum)
            for i in range(len(dic)+1, 20):
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 0, none)
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 1, none)
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 2, none)
            window.tableWidget_1.viewport().update()
            window.shishi_shangping_dic={}
            time.sleep(1)

class Thread_jiesuan(QThread):  # 计时器
    def __init__(self):
        super().__init__()

    def run(self):
        t1 = time.time()
        while True:
            t2 = time.time()
            if t2 - t1 >= 2:
                window.jiesuanlabel.clear()
                window.video_kaiguan=False
                break

class guanli_Window(QMainWindow):   # 管理员设置
    def __init__(self):
        super().__init__()
        loadUi('./images//guanliyuan.ui', self)
        self.setWindowIcon(QIcon('./icons/guanliyuan.png'))
        self.jiagebiao_show()
        self.IOU_lSlider.setValue(window.parameters['Iou'])
        self.IOU_lSlider.setTickInterval(10)
        self.IOU_lSlider.setTickPosition(QSlider.TicksBelow)
        self.label_IOU.setText(str(window.parameters['Iou']))
        self.Conf_Slider.setValue(window.parameters['Conf'])
        self.Conf_Slider.setTickInterval(10)
        self.Conf_Slider.setTickPosition(QSlider.TicksBelow)
        self.label_Conf.setText(str(window.parameters['Conf']))
        self.guanbishexiangtou.clicked.connect(self.stop_video)
        self.quedin.clicked.connect(self.jiagebiao_gai)
        self.IOU_lSlider.valueChanged.connect(self.Iou_gai)
        self.Conf_Slider.valueChanged.connect(self.Conf_gai)
        self.xiaoliang_tonji.clicked.connect(self.tonji_xiaoliang_show)
        self.guanbishexiangtou_2.clicked.connect(self.guanji)

    def stop_video(self):
        if window.video_kaiguan==True:
            window.video_kaiguan=False
            for i in range(20):
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 0, none)
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 1, none)
                none = QTableWidgetItem('')
                window.tableWidget_1.setItem(i, 2, none)
            window.tableWidget_1.viewport().update()
            window.shishi_shangping_dic={}

    def jiagebiao_show(self):
        dic=window.shangping_jiage
        for i,item in enumerate(dic):
            name = QTableWidgetItem(item)
            value=QTableWidgetItem(str(dic[item]))
            self.jiagebiao.setItem(i, 0, name)
            self.jiagebiao.setItem(i, 1, value)
        self.jiagebiao.update()

    def jiagebiao_gai(self):
        dic = window.shangping_jiage
        for i,item in enumerate(dic):
            value=float(self.jiagebiao.item(i, 1).text())
            window.shangping_jiage[item]=value
        self.label_quedin.setText('修改成功!')
        self.jiagebiao_show()
        self.thread_3 = Thread_2()
        self.thread_3.start()

    def Iou_gai(self):
        size = self.IOU_lSlider.value()/100
        window.parameters['Iou']=size
        self.label_IOU.setText(str(size))

    def Conf_gai(self):
        size = self.Conf_Slider.value()/100
        window.parameters['Conf']=size
        self.label_Conf.setText(str(size))

    def tonji_xiaoliang_show(self):
        window_tonji.tonji_show()
        window_tonji.show()

    def guanji(self):
        sys.exit()

class Thread_2(QThread):  # 计时器
    def __init__(self):
        super().__init__()

    def run(self):
        t1 = time.time()
        while True:
            t2 = time.time()
            if t2 - t1 >= 1:
                window_guanli.label_quedin.clear()
                break

class tonji_Window(QMainWindow):   # 管理员设置
    def __init__(self):
        super().__init__()
        loadUi('./images/xiaoshouliang.ui', self)
        self.setWindowIcon(QIcon('./icons/guanliyuan.png'))

    def tonji_show(self):
        df = pd.read_csv('xiaoshou.csv', index_col=0)
        dic = df.to_dict()['count']
        d_order = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        for i,item in enumerate(d_order):
            name = QTableWidgetItem(window.shangping[item[0]])
            value = QTableWidgetItem(str(item[1]))
            self.xiaoliangtonjibiao.setItem(i, 0, name)
            self.xiaoliangtonjibiao.setItem(i, 1, value)
        self.xiaoliangtonjibiao.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = MainWindow()

    window_guanli = guanli_Window()
    window_tonji=tonji_Window()
    window.showFullScreen()
    #window.show()
    app.exec()