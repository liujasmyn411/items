/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : wolin0323

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 24/04/2026 21:01:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for employment
-- ----------------------------
DROP TABLE IF EXISTS `employment`;
CREATE TABLE `employment`  (
  `employment_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '主键：就业ID',
  `student_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '外键：学生学号',
  `job_open_time` date NULL DEFAULT NULL COMMENT '就业开放时间',
  `offer_send_time` date NULL DEFAULT NULL COMMENT 'offer下发时间',
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '就业公司',
  `salary` int(0) NULL DEFAULT NULL COMMENT '就业薪资',
  `is_deleted` tinyint(0) NULL DEFAULT 0 COMMENT '逻辑删除 0-未删除 1-已删除',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`employment_id`) USING BTREE,
  INDEX `fk_employment_student`(`student_no`) USING BTREE,
  CONSTRAINT `fk_employment_student` FOREIGN KEY (`student_no`) REFERENCES `student` (`student_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '就业信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of employment
-- ----------------------------
INSERT INTO `employment` VALUES (1, 'S2025001', '2025-07-01', '2025-07-10', '百度', 15000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (2, 'S2025002', '2025-07-01', '2025-07-12', '阿里', 16000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (3, 'S2025003', '2025-07-01', '2025-07-11', '腾讯', 14500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (4, 'S2025004', '2025-07-01', '2025-07-15', '美团', 15500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (5, 'S2025005', '2025-07-10', '2025-07-20', '字节', 13000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (6, 'S2025006', '2025-07-10', '2025-07-22', '京东', 13500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (7, 'S2025007', '2025-07-10', '2025-07-18', '拼多多', 16000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (8, 'S2025008', '2025-07-10', '2025-07-25', '网易', 14000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (9, 'S2025009', '2025-07-15', '2025-07-28', '华为', 18000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (10, 'S2025010', '2025-07-15', '2025-07-30', '中兴', 17000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (11, 'S2025011', '2025-07-15', '2025-08-01', '浪潮', 15000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (12, 'S2025012', '2025-07-15', '2025-08-03', '科大讯飞', 16500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (13, 'S2025013', '2025-07-20', '2025-08-05', '小米', 14500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (14, 'S2025014', '2025-07-20', '2025-08-08', 'OV', 15500, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');
INSERT INTO `employment` VALUES (15, 'S2025015', '2025-07-20', '2025-08-10', '理想', 17000, 0, '2026-04-24 19:26:30', '2026-04-24 19:26:30');

SET FOREIGN_KEY_CHECKS = 1;
