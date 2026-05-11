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

 Date: 24/04/2026 21:02:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `teacher_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '主键：老师编号',
  `teacher_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '老师姓名',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `is_deleted` tinyint(0) NULL DEFAULT 0 COMMENT '逻辑删除 0-未删除 1-已删除',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`teacher_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '老师表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES (1, '张教授', '男', '13800001001', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (2, '李老师', '女', '13800001002', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (3, '王讲师', '男', '13800001003', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (4, '赵导师', '女', '13800001004', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (5, '刘主管', '男', '13800001005', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (6, '陈老师', '女', '13800001006', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (7, '杨教授', '男', '13800001007', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (8, '黄讲师', '女', '13800001008', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (9, '吴老师', '男', '13800001009', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (10, '周导师', '女', '13800001010', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (11, '徐主管', '男', '13800001011', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (12, '孙老师', '女', '13800001012', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (13, '马教授', '男', '13800001013', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (14, '朱讲师', '女', '13800001014', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `teacher` VALUES (15, '胡老师', '男', '13800001015', 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');

SET FOREIGN_KEY_CHECKS = 1;
