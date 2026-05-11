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

 Date: 24/04/2026 21:01:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for class_info
-- ----------------------------
DROP TABLE IF EXISTS `class_info`;
CREATE TABLE `class_info`  (
  `class_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '主键：班级编号',
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '班级名称',
  `start_time` date NULL DEFAULT NULL COMMENT '开课时间',
  `head_teacher_id` int(0) NULL DEFAULT NULL COMMENT '外键：班主任ID',
  `lecturer_id` int(0) NULL DEFAULT NULL COMMENT '外键：授课老师ID',
  `is_deleted` tinyint(0) NULL DEFAULT 0 COMMENT '逻辑删除 0-未删除 1-已删除',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`class_id`) USING BTREE,
  INDEX `fk_class_head_teacher`(`head_teacher_id`) USING BTREE,
  INDEX `fk_class_lecturer`(`lecturer_id`) USING BTREE,
  CONSTRAINT `fk_class_head_teacher` FOREIGN KEY (`head_teacher_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_class_lecturer` FOREIGN KEY (`lecturer_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '班级信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of class_info
-- ----------------------------
INSERT INTO `class_info` VALUES (1, 'Java全栈一班', '2025-02-01', 1, 2, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (2, 'Java全栈二班', '2025-02-01', 2, 3, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (3, '前端开发一班', '2025-02-10', 3, 4, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (4, '前端开发二班', '2025-02-10', 4, 5, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (5, '大数据一班', '2025-02-15', 5, 6, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (6, '大数据二班', '2025-02-15', 6, 7, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (7, 'Python一班', '2025-02-20', 7, 8, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (8, 'Python二班', '2025-02-20', 8, 9, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (9, '测试开发一班', '2025-02-25', 9, 10, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (10, '测试开发二班', '2025-02-25', 10, 11, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (11, '云计算一班', '2025-03-01', 11, 12, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (12, '云计算二班', '2025-03-01', 12, 13, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (13, '网络安全一班', '2025-03-05', 13, 14, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (14, '网络安全二班', '2025-03-05', 14, 15, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `class_info` VALUES (15, '人工智能一班', '2025-03-10', 15, 1, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');

SET FOREIGN_KEY_CHECKS = 1;
