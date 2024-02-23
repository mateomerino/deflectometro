-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-05-2023 a las 18:36:49
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `deflectometrodb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo`
--

CREATE TABLE `ciclo` (
  `nro_puesto` tinyint(4) NOT NULL,
  `nro_ciclo` int(11) NOT NULL DEFAULT 0,
  `codigo_prog` smallint(6) NOT NULL DEFAULT 0,
  `fecha_hora_inicio` datetime DEFAULT NULL,
  `fecha_hora_final` datetime DEFAULT NULL,
  `distancia_inicio` bigint(20) DEFAULT NULL,
  `distancia_final` bigint(20) DEFAULT NULL,
  `operario` varchar(50) DEFAULT NULL,
  `turno` varchar(15) DEFAULT NULL,
  `utilizar_en_estad` tinyint(4) NOT NULL DEFAULT 0,
  `campos_extra` text DEFAULT NULL,
  `nro_lote` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ciclo`
--

INSERT INTO `ciclo` (`nro_puesto`, `nro_ciclo`, `codigo_prog`, `fecha_hora_inicio`, `fecha_hora_final`, `distancia_inicio`, `distancia_final`, `operario`, `turno`, `utilizar_en_estad`, `campos_extra`, `nro_lote`) VALUES
(1, 56, 800, '2021-12-08 15:46:04', '2021-12-08 15:46:32', 2000, 2999, '1', 'MAÑANA', 1, '1', '1'),
(1, 57, 800, '2021-12-09 15:46:04', '2021-12-09 15:46:32', 3000, 3999, '1', 'MAÑANA', 1, '1', '1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mediciones_ciclo`
--

CREATE TABLE `mediciones_ciclo` (
  `nro_puesto` tinyint(4) NOT NULL DEFAULT 0,
  `nro_ciclo` int(11) NOT NULL DEFAULT 0,
  `nro_medicion` tinyint(4) NOT NULL DEFAULT 0,
  `valor` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mediciones_ciclo`
--

INSERT INTO `mediciones_ciclo` (`nro_puesto`, `nro_ciclo`, `nro_medicion`, `valor`) VALUES
(1, 56, 1, 51.0124),
(1, 56, 2, 51.0107),
(1, 56, 3, 31.5588),
(1, 57, 1, 51.0123),
(1, 57, 2, 51.0108),
(1, 57, 3, 31.5587);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ciclo`
--
ALTER TABLE `ciclo`
  ADD PRIMARY KEY (`nro_puesto`,`nro_ciclo`);

--
-- Indices de la tabla `mediciones_ciclo`
--
ALTER TABLE `mediciones_ciclo`
  ADD PRIMARY KEY (`nro_puesto`,`nro_ciclo`,`nro_medicion`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `mediciones_ciclo`
--
ALTER TABLE `mediciones_ciclo`
  ADD CONSTRAINT `mediciones_ciclo_ibfk_1` FOREIGN KEY (`nro_puesto`,`nro_ciclo`) REFERENCES `ciclo` (`nro_puesto`, `nro_ciclo`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
