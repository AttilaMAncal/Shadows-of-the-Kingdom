-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2025. Már 24. 15:13
-- Kiszolgáló verziója: 10.4.27-MariaDB
-- PHP verzió: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `game_data`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `game_save`
--

CREATE TABLE `game_save` (
  `id` int(11) NOT NULL,
  `health` int(11) DEFAULT NULL,
  `coins` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `time` float DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- A tábla adatainak kiíratása `game_save`
--

INSERT INTO `game_save` (`id`, `health`, `coins`, `level`, `time`, `timestamp`) VALUES
(1, 5, 9, 1, 26.01, '2025-03-23 10:56:14'),
(2, 4, 3, 2, 9.579, '2025-03-23 10:56:23'),
(3, 5, 10, 1, 32.583, '2025-03-23 10:57:24'),
(4, 4, 3, 2, 7.614, '2025-03-23 10:57:31'),
(5, 5, 8, 1, 25.843, '2025-03-23 11:02:05'),
(6, 5, 3, 2, 8.048, '2025-03-23 11:02:13'),
(7, 5, 8, 1, 25.938, '2025-03-23 15:21:46'),
(8, 4, 3, 2, 8.092, '2025-03-23 15:21:54'),
(9, 5, 8, 1, 26.107, '2025-03-24 12:56:35'),
(10, 5, 3, 2, 7.227, '2025-03-24 12:56:43'),
(11, 5, 8, 1, 24.715, '2025-03-24 13:02:04'),
(12, 4, 3, 2, 6.779, '2025-03-24 13:02:11'),
(13, 5, 8, 1, 25.986, '2025-03-24 13:29:28'),
(14, 5, 11, 1, 34.301, '2025-03-24 13:31:37'),
(15, 2, 12, 2, 62.512, '2025-03-24 13:32:40'),
(16, 4, 8, 1, 28.579, '2025-03-24 13:40:15'),
(17, 4, 7, 2, 46.968, '2025-03-24 13:41:03'),
(18, 4, 8, 1, 25.517, '2025-03-24 13:42:00'),
(19, 4, 4, 2, 28.782, '2025-03-24 13:42:29'),
(20, 5, 8, 1, 26.702, '2025-03-24 14:01:21');

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `game_save`
--
ALTER TABLE `game_save`
  ADD PRIMARY KEY (`id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `game_save`
--
ALTER TABLE `game_save`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
