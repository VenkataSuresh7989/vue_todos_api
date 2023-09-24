-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 24, 2023 at 09:07 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vue_crud`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `created_at` varchar(20) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `updated_at` varchar(20) NOT NULL,
  `updated_by` varchar(20) NOT NULL,
  `status` enum('1','0') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`) VALUES
(1, 'Samsung M32', '2023-08-27 20:15:58', '', '2023-08-28 20:05:47', 'admin', '0'),
(2, 'iPhone 123', '2023-08-26 21:42:15', 'admin', '2023-08-28 19:52:48', 'admin', '0'),
(3, 'VIVO', '2023-08-27 21:36:05', 'admin', '', '', '0'),
(5, 'Oneplus', '2023-08-28 20:06:06', 'admin', '2023-08-28 20:06:24', 'admin', '0'),
(6, 'Test', '2023-09-23 16:30:55', 'admin', '2023-09-23 16:32:03', 'admin', '1');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(15) NOT NULL,
  `full_name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `hashed_password` varchar(100) NOT NULL,
  `disabled` enum('False','True') NOT NULL,
  `created_at` varchar(20) NOT NULL,
  `created_by` varchar(30) NOT NULL,
  `updated_at` varchar(20) NOT NULL,
  `updated_by` varchar(30) NOT NULL,
  `status` enum('0','1') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `email`, `hashed_password`, `disabled`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`) VALUES
(1, 'suresh', 'venkat suresh7989', 'suresh@gmail.com', 'gAAAAABlD9QQtUUAoonxkMp_hdAn_RSL6xn2Cbz__SVE9pb7QZI3DmDfdHOSMCJo9oOgJcky352ljc_Z0q-Vt3z76EDQRrxKzg==', 'False', '2023-08-27 16:41:50', 'admin', '2023-09-24 11:55:23', 'suresh', '0'),
(3, 'sai krishna', 'Mohan Roy', 'mohan@gmail.com', 'gAAAAABlB9eR89WrOzcTlq_yHEaGYxqmqeb9pfcCWAvtIQJ3JSdt9ZfpKDKVYJ3VNtjHItFGZfI3IP3XCzYiywFfr-uUzOuPnQ==', 'False', '2023-08-27 17:58:28', 'admin', '2023-08-27 19:36:47', 'sai krishna', '0'),
(4, 'venkat', 'venkat', 'venkat@gmail.com', 'gAAAAABlB9dxDo9ClO12lTyp6W6KDlDL7rnQhztkiDbrTtL9crgsSCRxNsXuyjQm4oR58wrPKYqP6nEF1TMfY2OCuXorbDYaMQ==', 'False', '2023-09-09 16:49:15', 'admin', '', '', '0'),
(6, 'demo', 'demo', 'demo@gmail.com', 'gAAAAABlD9NKP9vZc0ZJepfrhNoFAsB0ZJhoHcU3_vr_T97lQ7e5vg6nwZ_dUc5DaTsE1jd_S4Y6RW5j3iD1cP4-sYAoEVw9hg==', 'False', '2023-09-24 11:42:26', 'admin', '', '', '0');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
