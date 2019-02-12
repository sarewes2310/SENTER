-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 31 Jan 2019 pada 03.24
-- Versi Server: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sentiment_analysis_twitter`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `hashtag`
--


-- --------------------------------------------------------

--
-- Struktur dari tabel `retweet`
--

--CREATE TABLE `retweet` (
--  `idR` int(60) NOT NULL,
--  `idT` int(60) NOT NULL,
--  `Username` varchar(50) NOT NULL,
--  `retweet` text NOT NULL,
--  `SA` varchar(20) NOT NULL
--) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tweet`
--

CREATE TABLE `tweet` (
  `idT` int(60) NOT NULL,
  `id` int(60) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `tanggal` date NOT NULL,  
  `tweet` text NOT NULL,
  `hashtag` text NOT NULL,
  `RT` int(20) NOT NULL,
  `SA` varchar(20) NOT NULL,
  `SAP` float NOT NULL
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

-- AUTO_INCREMENT for table `tweet`
--

ALTER TABLE `tweet`
  ADD PRIMARY KEY (`idT`);


ALTER TABLE `tweet`
  MODIFY `idT` int(60) NOT NULL AUTO_INCREMENT;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
