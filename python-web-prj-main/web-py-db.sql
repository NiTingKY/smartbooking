/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50736
Source Host           : localhost:3306
Source Database       : web-py-db

Target Server Type    : MYSQL
Target Server Version : 50736
File Encoding         : 65001

Date: 2025-05-26 11:41:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for chat
-- ----------------------------
DROP TABLE IF EXISTS `chat`;
CREATE TABLE `chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of chat
-- ----------------------------

-- ----------------------------
-- Table structure for item
-- ----------------------------
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `dollar` decimal(10,2) NOT NULL COMMENT '金额',
  `plat` varchar(255) DEFAULT NULL COMMENT '平台',
  `detail` text COMMENT '明细',
  `source` varchar(255) DEFAULT NULL COMMENT '来源',
  `is_income` tinyint(1) NOT NULL DEFAULT '0' COMMENT '收入标识',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`uid`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of item
-- ----------------------------
INSERT INTO `item` VALUES ('1', '128.50', '支付宝', '超市购物', '购物', '0', '1', '2025-05-01 09:30:45', '2025-05-25 12:58:02', '1');
INSERT INTO `item` VALUES ('2', '2500.00', '银行转账', '工资收入', '薪资', '1', '0', '2025-05-05 15:20:10', '2025-05-05 15:20:10', '1');
INSERT INTO `item` VALUES ('3', '65.80', '微信支付', '午餐外卖', '餐饮', '0', '0', '2025-05-10 12:15:30', '2025-05-10 12:15:30', '2');
INSERT INTO `item` VALUES ('4', '300.00', '现金', '交通卡充值', '交通', '0', '0', '2025-05-15 08:45:00', '2025-05-15 08:45:00', '2');
INSERT INTO `item` VALUES ('5', '1500.00', 'PayPal', '项目奖金', '额外收入', '1', '0', '2025-05-20 17:00:00', '2025-05-20 17:00:00', '1');
INSERT INTO `item` VALUES ('6', '89.90', '京东白条', '书籍购买', '教育', '0', '0', '2025-04-25 20:10:15', '2025-05-22 20:36:09', '2');
INSERT INTO `item` VALUES ('7', '4200.00', '银行转账', '工资收入', '公司账户', '1', '0', '2025-05-20 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('8', '198.50', '微信支付', '午餐消费', '麦当劳', '0', '0', '2025-04-21 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('9', '1500.00', '支付宝', '兼职收入', '设计项目', '1', '1', '2025-03-23 20:32:10', '2025-05-26 11:16:54', '1');
INSERT INTO `item` VALUES ('10', '650.00', '现金', '交通费用', '出租车', '0', '0', '2025-04-22 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('11', '99.90', '信用卡', '网购消费', '淘宝', '0', '0', '2025-01-25 20:32:10', '2025-05-22 20:36:16', '1');
INSERT INTO `item` VALUES ('12', '3200.00', '银行转账', '项目奖金', '客户付款', '1', '0', '2025-05-02 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('13', '299.00', '微信支付', '电影票', '电影院', '0', '0', '2025-05-07 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('14', '1800.00', '支付宝', '稿费收入', '出版社', '1', '0', '2025-01-04 20:32:10', '2025-05-22 20:36:20', '1');
INSERT INTO `item` VALUES ('15', '450.00', '现金', '超市购物', '家乐福', '0', '0', '2025-04-06 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('16', '2500.00', '银行转账', '投资回报', '理财平台', '1', '0', '2025-02-27 20:32:10', '2025-05-22 20:32:10', '1');
INSERT INTO `item` VALUES ('17', '385.00', '微信支付', '咖啡消费', '星巴克', '0', '0', '2025-03-02 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('18', '2200.00', '银行转账', '奖金收入', '公司账户', '1', '0', '2025-05-13 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('19', '799.00', '支付宝', '电子产品', '京东', '0', '0', '2025-03-10 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('20', '1500.00', 'PayPal', '外包收入', '自由职业', '1', '0', '2025-03-13 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('21', '95.50', '现金', '日用品', '便利店', '0', '0', '2025-04-13 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('22', '2800.00', '银行转账', '项目结算', '客户A', '1', '0', '2025-03-08 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('23', '450.00', '信用卡', '服装消费', '优衣库', '0', '0', '2025-03-03 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('24', '1800.00', '微信支付', '设计收入', '客户B', '1', '0', '2025-02-27 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('25', '650.00', '支付宝', '交通卡充值', '地铁站', '0', '0', '2025-05-19 20:35:05', '2025-05-22 20:35:05', '1');
INSERT INTO `item` VALUES ('26', '3200.00', '银行转账', '投资分红', '证券公司', '1', '0', '2025-01-20 20:35:05', '2025-05-22 20:35:50', '1');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `account` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `sex` varchar(255) DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  `valid` int(11) DEFAULT '1',
  `photo_adr` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uid`) USING BTREE,
  UNIQUE KEY `account` (`account`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'user1', '123', '123456', '17735841695', '9rq5m7tb@outlook.com', 'woman', '2025-04-29 10:51:57', '1', 'http://localhost:5000/static/photo.png');
INSERT INTO `user` VALUES ('2', 'user2', '234', '123456', '12830187965', '1zqem690gm@qq.com', 'man', '2025-04-20 10:51:57', '1', 'http://localhost:5000/static/photo.png');
INSERT INTO `user` VALUES ('3', 'test_add', '13131', '13131231', '112312313', '12313@12313.com', 'man', '2025-04-30 16:00:00', '1', 'http://localhost:5000/static/photo.png');
INSERT INTO `user` VALUES ('4', 'user_test_add', '12312312313', '123131313', '123131313', '231313@12313.com', 'man', '2025-04-30 16:00:00', '1', 'http://localhost:5000/static/photo.png');
