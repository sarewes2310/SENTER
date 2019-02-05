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

CREATE TABLE `hashtag` (
  `idH` int(60) NOT NULL,
  `isi` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `retweet`
--

CREATE TABLE `retweet` (
  `idR` int(60) NOT NULL,
  `idT` int(60) NOT NULL,
  `screenName` varchar(50) NOT NULL,
  `retweet` text NOT NULL,
  `sentiment` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tweet`
--

CREATE TABLE `tweet` (
  `idT` int(60) NOT NULL,
  `idH` int(60) NOT NULL,
  `tweet` text NOT NULL,
  `screenName` varchar(50) NOT NULL,
  `countR` int(20) NOT NULL,
  `sentiment` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hashtag`
--
ALTER TABLE `hashtag`
  ADD PRIMARY KEY (`idH`);

--
-- Indexes for table `retweet`
--
ALTER TABLE `retweet`
  ADD PRIMARY KEY (`idR`),
  ADD KEY `idT` (`idT`);

--
-- Indexes for table `tweet`
--
ALTER TABLE `tweet`
  ADD PRIMARY KEY (`idT`),
  ADD KEY `idH` (`idH`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hashtag`
--
ALTER TABLE `hashtag`
  MODIFY `idH` int(60) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `retweet`
--
ALTER TABLE `retweet`
  MODIFY `idR` int(60) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tweet`
--
ALTER TABLE `tweet`
  MODIFY `idT` int(60) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `retweet`
--
ALTER TABLE `retweet`
  ADD CONSTRAINT `idT` FOREIGN KEY (`idT`) REFERENCES `tweet` (`idT`);

--
-- Ketidakleluasaan untuk tabel `tweet`
--
ALTER TABLE `tweet`
  ADD CONSTRAINT `idH` FOREIGN KEY (`idH`) REFERENCES `hashtag` (`idH`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
