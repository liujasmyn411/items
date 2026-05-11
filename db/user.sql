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

 Date: 06/05/2026 14:08:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户主键ID',
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录账号',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录密码(MD5加密)',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像地址',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色：manager管理员 / teacher老师 / student学生',
  `ref_id` int(0) NULL DEFAULT NULL COMMENT '关联业务表主键：老师teacher_id / 学生id',
  `is_deleted` tinyint(0) NULL DEFAULT 0 COMMENT '逻辑删除 0正常 1删除',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  INDEX `fk_user_student`(`ref_id`) USING BTREE,
  CONSTRAINT `fk_user_student` FOREIGN KEY (`ref_id`) REFERENCES `student` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `fk_user_teacher` FOREIGN KEY (`ref_id`) REFERENCES `teacher` (`teacher_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统登录用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin01', '21218cca77804d2ba949f7c451c22119', '/static/avatars/admin1.png', '13511110001', 'manager', NULL, 1, '2026-04-25 20:09:31', '2026-04-28 14:22:26');
INSERT INTO `user` VALUES (2, 'admin02', '827ccb0eea8a706c4c34a16891f84e7b', '/static/avatars/admin2.png', '13511110002', 'manager', NULL, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (3, 'admin03', 'd8578edf8458ce06fbc5bb76a58c5ca4', NULL, '13511110003', 'manager', NULL, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (4, 'a_zhangjg', 'e10adc3949ba59abbe56e057f20f883e', 'static/avatars/Jasmyn.jpg', 'string', 'teacher', 1, 0, '2026-04-25 20:09:31', '2026-04-27 20:07:23');
INSERT INTO `user` VALUES (5, 't_lihm', '32532f9c479602f9d66f54c484388749', '/static/avatars/t2.png', '13800001002', 'teacher', 2, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (6, 't_wanght', '5f4dcc3b5aa765d61d8327deb882cf99', NULL, '13800001003', 'teacher', 3, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (7, 't_liuml', '7c4a8d09ca3762af61e59520943dc264', '/static/avatars/t4.png', '13800001004', 'teacher', 4, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (8, 't_chenzq', 'b123d30e8f57ed922a57b39f5cdf2f53', '/static/avatars/t5.png', '13800001005', 'teacher', 5, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (9, 's_zhangsan', '674f3b3f8c2a56128b44b4f0a95f827c', '/static/avatars/s1.png', '13611112001', 'student', 1, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (10, 's_lisi', '1f3870be274f4c4af3f633f21f6c03ae', '/static/avatars/s2.png', '13611112002', 'student', 2, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (11, 's_wangwu', 'c33367701511b6f37637f9f8f32ade22', NULL, '13611112003', 'student', 3, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (12, 's_zhaoliu', '4a7d1ed414474e4033db5f4d9027a10b', '/static/avatars/s4.png', '13611112004', 'student', 4, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (13, 's_sunqi', '163b7a940e573812e046202406099965', '/static/avatars/s5.png', '13611112005', 'student', 5, 0, '2026-04-25 20:09:31', '2026-04-25 20:09:31');
INSERT INTO `user` VALUES (14, 'admin10', '827ccb0eea8a706c4c34a16891f84e7b', 'static/avatars/Jasmyn.jpg', 'string', 'manager', NULL, 0, '2026-04-27 13:37:33', '2026-04-27 13:37:33');
INSERT INTO `user` VALUES (15, 'admin13', 'b45cffe084dd3d20d928bee85e7b0f21', 'static/avatars/elvis.jpg', 'string', 'manager', NULL, 1, '2026-04-27 13:37:45', '2026-04-27 13:51:20');
INSERT INTO `user` VALUES (17, 'teacher', '827ccb0eea8a706c4c34a16891f84e7b', 'static/avatars/Sam.jpg', 'string', 'teacher', NULL, 0, '2026-04-27 14:05:26', '2026-04-27 14:05:26');
INSERT INTO `user` VALUES (18, '8099909', 'b45cffe084dd3d20d928bee85e7b0f21', 'static/avatars/Cedric.jpg', '0', 'student', NULL, 1, '2026-04-27 15:02:58', '2026-04-27 20:09:17');
INSERT INTO `user` VALUES (19, 'aseeee', 'b45cffe084dd3d20d928bee85e7b0f21', 'static/avatars/Cedric.jpg', '0', 'student', NULL, 0, '2026-04-27 15:03:12', '2026-04-27 15:03:12');
INSERT INTO `user` VALUES (20, '66666', 'b45cffe084dd3d20d928bee85e7b0f21', 'static/avatars/AC.jpg', 'iii', 'student', 8, 0, '2026-04-27 15:07:41', '2026-04-28 17:20:14');
INSERT INTO `user` VALUES (21, 'asddffff', '827ccb0eea8a706c4c34a16891f84e7b', 'static/avatars/AC.jpg', '0', 'student', 9, 0, '2026-04-27 15:09:18', '2026-04-27 15:09:18');
INSERT INTO `user` VALUES (24, 'yuiyiu', '36ab85d48f43fb8b792b05eaa32d8972', 'static/avatars/Jasmyn.jpg', '0', 'student', 10, 0, '2026-04-27 15:15:49', '2026-04-27 15:15:49');
INSERT INTO `user` VALUES (25, 'tttyty', '40d167ba137a287032ca198a6654c20c', 'static/avatars/Jiayi.jpg', '0', 'student', 11, 0, '2026-04-27 15:18:17', '2026-04-27 15:18:17');
INSERT INTO `user` VALUES (26, 'opoopoop1', '7c51a5e6ea3214af970a86df89793b19', 'static/avatars/Jasmyn.jpg', '0', 'teacher', 6, 0, '2026-04-27 15:21:14', '2026-04-28 19:28:59');
INSERT INTO `user` VALUES (27, 'iiijj', 'b3275960d68fda9d831facc0426c3bbc', 'static/avatars/Qi Zhou.jpg', '0', 'student', 7, 1, '2026-04-27 15:22:51', '2026-04-27 18:48:05');
INSERT INTO `user` VALUES (28, 'jgdssaa1', 'e10adc3949ba59abbe56e057f20f883e', 'static/avatars/Jiayi.jpg', '0', 'student', 12, 0, '2026-04-27 15:30:27', '2026-04-28 19:25:54');
INSERT INTO `user` VALUES (29, 'qwertt', '827ccb0eea8a706c4c34a16891f84e7b', 'static/avatars/elvis.jpg', '0', 'teacher', 8, 0, '2026-04-27 15:36:19', '2026-04-27 15:36:19');
INSERT INTO `user` VALUES (30, 'root1', '25d55ad283aa400af464c76d713c07ad', 'static/avatars/差不多。.jpg', '123456', 'student', 13, 1, '2026-04-28 07:39:09', '2026-04-28 14:19:36');
INSERT INTO `user` VALUES (34, 'root', '827ccb0eea8a706c4c34a16891f84e7b', 'static/avatars/dream.jpg', '17822442026', 'student', 14, 1, '2026-04-28 17:07:38', '2026-04-28 20:21:03');
INSERT INTO `user` VALUES (35, 'qykkkkk', 'e10adc3949ba59abbe56e057f20f883e', 'static/avatars/CyberOrange.jpg', '12345678912', 'teacher', 15, 1, '2026-04-28 20:05:17', '2026-04-28 20:10:56');
INSERT INTO `user` VALUES (36, 'bili', '3fd28eac7aac3f38eca83206e27638fd', 'static/avatars/CyberOrange.jpg', '17875661612', 'teacher', 9, 0, '2026-05-05 18:57:26', '2026-05-05 18:57:26');
INSERT INTO `user` VALUES (44, '123456', 'e10adc3949ba59abbe56e057f20f883e', 'static/avatars/Cedric.jpg', NULL, 'teacher', 11, 0, '2026-05-06 11:52:32', '2026-05-06 11:52:32');

SET FOREIGN_KEY_CHECKS = 1;
