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

 Date: 24/04/2026 21:02:01
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '主键：学生编号',
  `student_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '业务学号（唯一）',
  `class_id` int(0) NULL DEFAULT NULL COMMENT '外键：班级ID',
  `student_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学生姓名',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `age` int(0) NULL DEFAULT NULL COMMENT '年龄',
  `native_place` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '籍贯',
  `graduate_school` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '毕业院校',
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '专业',
  `education` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学历',
  `admission_time` date NULL DEFAULT NULL COMMENT '入学时间',
  `graduate_time` date NULL DEFAULT NULL COMMENT '毕业时间',
  `advisor_id` int(0) NULL DEFAULT NULL COMMENT '外键：顾问老师ID',
  `is_deleted` tinyint(0) NULL DEFAULT 0 COMMENT '逻辑删除 0-未删除 1-已删除',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_student_no`(`student_no`) USING BTREE,
  INDEX `fk_student_class`(`class_id`) USING BTREE,
  INDEX `fk_student_advisor`(`advisor_id`) USING BTREE,
  CONSTRAINT `fk_student_advisor` FOREIGN KEY (`advisor_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_student_class` FOREIGN KEY (`class_id`) REFERENCES `class_info` (`class_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '学生表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (1, 'S2025001', 1, '张三', '男', 22, '北京', '北京理工大学', '计算机', '本科', '2025-02-01', '2025-08-01', 1, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (2, 'S2025002', 1, '李四', '女', 21, '上海', '上海大学', '软件工程', '本科', '2025-02-01', '2025-08-01', 2, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (3, 'S2025003', 2, '王五', '男', 23, '广州', '中山大学', '电子信息', '本科', '2025-02-01', '2025-08-01', 3, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (4, 'S2025004', 2, '赵六', '女', 22, '深圳', '深圳大学', '通信工程', '本科', '2025-02-01', '2025-08-01', 4, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (5, 'S2025005', 3, '孙七', '男', 20, '杭州', '浙江大学', '自动化', '专科', '2025-02-10', '2025-08-10', 5, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (6, 'S2025006', 3, '周八', '女', 21, '南京', '南京大学', '物联网', '专科', '2025-02-10', '2025-08-10', 6, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (7, 'S2025007', 4, '吴九', '男', 22, '成都', '四川大学', '计算机', '本科', '2025-02-10', '2025-08-10', 7, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (8, 'S2025008', 4, '郑十', '女', 23, '重庆', '重庆大学', '软件工程', '本科', '2025-02-10', '2025-08-10', 8, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (9, 'S2025009', 5, '冯十一', '男', 21, '武汉', '武汉大学', '电子信息', '本科', '2025-02-15', '2025-08-15', 9, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (10, 'S2025010', 5, '陈十二', '女', 22, '西安', '西安电子科大', '通信工程', '本科', '2025-02-15', '2025-08-15', 10, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (11, 'S2025011', 6, '褚十三', '男', 24, '济南', '山东大学', '自动化', '本科', '2025-02-15', '2025-08-15', 11, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (12, 'S2025012', 6, '卫十四', '女', 23, '福州', '福州大学', '物联网', '专科', '2025-02-15', '2025-08-15', 12, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (13, 'S2025013', 7, '蒋十五', '男', 22, '郑州', '郑州大学', '计算机', '本科', '2025-02-20', '2025-08-20', 13, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (14, 'S2025014', 7, '沈十六', '女', 21, '长沙', '湖南大学', '软件工程', '专科', '2025-02-20', '2025-08-20', 14, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');
INSERT INTO `student` VALUES (15, 'S2025015', 8, '韩十七', '男', 23, '石家庄', '河北工大', '电子信息', '本科', '2025-02-20', '2025-08-20', 15, 0, '2026-04-24 19:26:29', '2026-04-24 19:26:29');

SET FOREIGN_KEY_CHECKS = 1;
