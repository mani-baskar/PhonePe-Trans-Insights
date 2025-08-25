START TRANSACTION;

-- =========================
-- Core tables (with PK/AUTO_INCREMENT inline)
-- =========================

CREATE TABLE IF NOT EXISTS `agg_ins` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `from_ts` bigint(20) DEFAULT NULL,
  `to_ts` bigint(20) DEFAULT NULL,
  `insurance_name` varchar(100) DEFAULT NULL,
  `payment_type` varchar(50) DEFAULT NULL,
  `payment_count` bigint(20) DEFAULT NULL,
  `payment_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `agg_trans` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `from_ts` bigint(20) DEFAULT NULL,
  `to_ts` bigint(20) DEFAULT NULL,
  `transaction_name` varchar(100) DEFAULT NULL,
  `payment_type` varchar(50) DEFAULT NULL,
  `payment_count` bigint(20) DEFAULT NULL,
  `payment_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `agg_user` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `registered_users` bigint(20) DEFAULT NULL,
  `app_opens` bigint(20) DEFAULT NULL,
  `users_by_device` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`users_by_device`)),
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `map_ins_cntry` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `data_level` varchar(50) DEFAULT NULL,
  `grid_level` int(11) DEFAULT NULL,
  `percentiles` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`percentiles`)),
  `latitude` decimal(15,8) DEFAULT NULL,
  `longitude` decimal(15,8) DEFAULT NULL,
  `metric_value` decimal(20,2) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `map_ins_hover` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `location_name` varchar(100) DEFAULT NULL,
  `metric_type` varchar(50) DEFAULT NULL,
  `metric_count` bigint(20) DEFAULT NULL,
  `metric_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `map_trans` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `location_name` varchar(100) DEFAULT NULL,
  `metric_type` varchar(50) DEFAULT NULL,
  `metric_count` bigint(20) DEFAULT NULL,
  `metric_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `map_user` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `hover_state` varchar(100) DEFAULT NULL,
  `registered_users` bigint(20) DEFAULT NULL,
  `app_opens` bigint(20) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `top_ins` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `state_entity` varchar(100) DEFAULT NULL,
  `state_metric_type` varchar(50) DEFAULT NULL,
  `state_metric_count` bigint(20) DEFAULT NULL,
  `state_metric_amount` decimal(20,2) DEFAULT NULL,
  `district_entity` varchar(100) DEFAULT NULL,
  `district_metric_type` varchar(50) DEFAULT NULL,
  `district_metric_count` bigint(20) DEFAULT NULL,
  `district_metric_amount` decimal(20,2) DEFAULT NULL,
  `pincode_entity` varchar(10) DEFAULT NULL,
  `pincode_metric_type` varchar(50) DEFAULT NULL,
  `pincode_metric_count` bigint(20) DEFAULT NULL,
  `pincode_metric_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- >>> ADDED (was missing in your file) <<<
CREATE TABLE IF NOT EXISTS `top_trans` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `state_entity` varchar(100) DEFAULT NULL,
  `state_metric_type` varchar(50) DEFAULT NULL,
  `state_metric_count` bigint(20) DEFAULT NULL,
  `state_metric_amount` decimal(20,2) DEFAULT NULL,
  `district_entity` varchar(100) DEFAULT NULL,
  `district_metric_type` varchar(50) DEFAULT NULL,
  `district_metric_count` bigint(20) DEFAULT NULL,
  `district_metric_amount` decimal(20,2) DEFAULT NULL,
  `pincode_entity` varchar(10) DEFAULT NULL,
  `pincode_metric_type` varchar(50) DEFAULT NULL,
  `pincode_metric_count` bigint(20) DEFAULT NULL,
  `pincode_metric_amount` decimal(20,2) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

CREATE TABLE IF NOT EXISTS `top_user` (
  `sl_no` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `quarter` tinyint(4) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `state_name` varchar(100) DEFAULT NULL,
  `state_registered_users` bigint(20) DEFAULT NULL,
  `district_name` varchar(100) DEFAULT NULL,
  `district_registered_users` bigint(20) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `pincode_registered_users` bigint(20) DEFAULT NULL,
  `response_ts` bigint(20) DEFAULT NULL,
  `record_ts` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- =========================
-- Secondary indexes
-- (works on MariaDB 10.5+: IF NOT EXISTS)
-- =========================

CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `agg_ins`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `agg_trans`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `agg_user`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `map_ins_cntry`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `map_ins_hover`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `map_trans`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `map_user`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `top_ins`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `top_trans`(`state`,`year`,`quarter`);
CREATE INDEX IF NOT EXISTS `idx_state_year_quarter` ON `top_user`(`state`,`year`,`quarter`);

COMMIT;
