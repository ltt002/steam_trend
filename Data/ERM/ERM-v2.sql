CREATE TABLE `M_Game` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `GameName` string NOT NULL COMMENT '遊戲名稱',
  `OperationDate` date COMMENT '發行日'
);

CREATE TABLE `M_Category` (
  `CategoryID` string PRIMARY KEY NOT NULL COMMENT '自己編',
  `Category` string NOT NULL COMMENT '動作/角色扮演...'
);

CREATE TABLE `M_Tag` (
  `TagID` string PRIMARY KEY NOT NULL,
  `Tag` string NOT NULL
);

CREATE TABLE `M_Platform` (
  `PlatformID` string PRIMARY KEY NOT NULL,
  `Platform` string NOT NULL
);

CREATE TABLE `M_Country` (
  `CountryID` string PRIMARY KEY NOT NULL,
  `Country` string NOT NULL
);

CREATE TABLE `Transaction_byDate` (
  `UUID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `GameID` string NOT NULL,
  `Cost` int64 COMMENT '價錢',
  `MostPlayedRank` int64 NOT NULL COMMENT '人數排名',
  `HoursPlayed` int64 NOT NULL COMMENT '30天總遊玩時數',
  `PeakPlayers` int64 NOT NULL COMMENT '本日人數高峰',
  `AllTimePeak` int64 NOT NULL COMMENT '由始以來最高',
  `Viewers_Steam` int64 NOT NULL COMMENT 'Steam觀看人數',
  `TwitchRank` int64 NOT NULL COMMENT 'Twitch觀看排名',
  `ViewersTwitch` int64 NOT NULL COMMENT 'Twitch觀看人數',
  `Twitch24HoursPeak` int64 NOT NULL COMMENT 'Twitch24小時高峰人數',
  `Twitch_AllTimePeak` int64 NOT NULL COMMENT 'Twitch由始以來高峰',
  `Date` date NOT NULL COMMENT '日期'
);

CREATE TABLE `TopSell_byDate` (
  `UUID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `GameID` string NOT NULL,
  `Rank` int64 NOT NULL COMMENT '銷售排名',
  `CountryID` string NOT NULL COMMENT '國家ID',
  `Date` date NOT NULL COMMENT '日期'
);

CREATE TABLE `Players_byMonth` (
  `UUID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `GameID` string NOT NULL,
  `AvgPlayers` int64 NOT NULL COMMENT '每月平均人數',
  `PeakPlayers` string NOT NULL COMMENT '每月最高人數',
  `Date` date NOT NULL COMMENT '日期(xxxx-xx)'
);

CREATE TABLE `Game_withRated` (
  `GameID` int64 PRIMARY KEY NOT NULL COMMENT '評分排名',
  `Positive` int64 NOT NULL COMMENT '正面評論數',
  `Negative` int64 NOT NULL COMMENT '負面評論數',
  `Total` int64 NOT NULL COMMENT '全部評論數',
  `Rating` numeric NOT NULL COMMENT '評級'
);

CREATE TABLE `Game_withTag` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `TagID` string NOT NULL COMMENT 'Tag ID',
  PRIMARY KEY (`GameID`, `TagID`)
);

CREATE TABLE `Game_withCategory` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `CategoryID` string NOT NULL COMMENT '類型ID',
  PRIMARY KEY (`GameID`, `CategoryID`)
);

CREATE TABLE `Game_withPlatform` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `PlatformID` string NOT NULL COMMENT '平台ID',
  PRIMARY KEY (`GameID`, `PlatformID`)
);

ALTER TABLE `Transaction_byDate` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `TopSell_byDate` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `Players_byMonth` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `Game_withTag` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `Game_withCategory` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `Game_withPlatform` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `Game_withRated` ADD FOREIGN KEY (`GameID`) REFERENCES `M_Game` (`GameID`);

ALTER TABLE `TopSell_byDate` ADD FOREIGN KEY (`CountryID`) REFERENCES `M_Country` (`CountryID`);

ALTER TABLE `Game_withTag` ADD FOREIGN KEY (`TagID`) REFERENCES `M_Tag` (`TagID`);

ALTER TABLE `Game_withCategory` ADD FOREIGN KEY (`CategoryID`) REFERENCES `M_Category` (`CategoryID`);

ALTER TABLE `Game_withPlatform` ADD FOREIGN KEY (`PlatformID`) REFERENCES `M_Platform` (`PlatformID`);
