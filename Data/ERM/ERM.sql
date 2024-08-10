CREATE TABLE `主機遊戲` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `GameName` string NOT NULL COMMENT '遊戲名稱',
  `OperationDate` date COMMENT '發行日'
);

CREATE TABLE `Tem_Transfer` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `SteamName` string NOT NULL COMMENT '遊戲名稱',
  `SteamBroadcastName` string NOT NULL COMMENT 'steam直播遊戲名稱',
  `TwichName` string NOT NULL COMMENT 'twich直播遊戲名稱',
  `MobyName` string NOT NULL COMMENT 'Moby遊戲名稱'
);

CREATE TABLE `主檔_類別` (
  `CategoryID` string PRIMARY KEY NOT NULL COMMENT '自己編',
  `Category` string NOT NULL COMMENT '動作/角色扮演...'
);

CREATE TABLE `主檔_標籤` (
  `TagID` string PRIMARY KEY NOT NULL COMMENT '自己編',
  `Tag` string NOT NULL
);

CREATE TABLE `主檔_平台` (
  `SystemID` string PRIMARY KEY NOT NULL COMMENT '自己編',
  `System` string NOT NULL COMMENT 'Windows/mac...'
);

CREATE TABLE `主檔_國家` (
  `CountryID` string PRIMARY KEY NOT NULL COMMENT 'TW/HK...',
  `Country` string NOT NULL COMMENT 'Taiwan/Honkong...'
);

CREATE TABLE `Cost_by_Date` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `Cost` int NOT NULL COMMENT '價錢',
  `Date` date NOT NULL COMMENT '日期',
  PRIMARY KEY (`GameID`, `Date`)
);

CREATE TABLE `TopSale_by_Date` (
  `UUID` string PRIMARY KEY NOT NULL,
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `Rank` int NOT NULL COMMENT '銷售排名',
  `Country` string NOT NULL COMMENT '國家',
  `Date` date NOT NULL COMMENT '日期'
);

CREATE TABLE `HourPlayed_by_Date` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `HoursPlayed` int NOT NULL COMMENT '30天總遊玩時數',
  `Date` date NOT NULL COMMENT '日期',
  PRIMARY KEY (`GameID`, `Date`)
);

CREATE TABLE `MostPlayed_by_Date` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `Rank` int NOT NULL COMMENT '人數排名',
  `PeakPlayers` int NOT NULL COMMENT '本日人數高峰',
  `AllTimePeak` int NOT NULL COMMENT '由始以來最高',
  `Date` date NOT NULL COMMENT '日期'
);

CREATE TABLE `Steam_Broadcast_by_Date` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `SteamCurrentViewers` int NOT NULL COMMENT 'Steam觀看人數',
  `Date` date NOT NULL COMMENT '日期',
  PRIMARY KEY (`GameID`, `Date`)
);

CREATE TABLE `Twitch_by_Date` (
  `GameID` string NOT NULL COMMENT '遊戲ID',
  `Rank` int NOT NULL COMMENT 'Twitch觀看排名',
  `TwitchCurrentViewers` int NOT NULL COMMENT 'Twitch觀看人數',
  `Twitch24HoursPeak` int NOT NULL COMMENT 'Twitch24小時高峰人數',
  `AllTimePeak` int NOT NULL COMMENT 'Twitch由始以來高峰人數',
  `Date` date NOT NULL COMMENT '日期',
  PRIMARY KEY (`GameID`, `Date`)
);

CREATE TABLE `Game_with_Tag` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `TagID` string NOT NULL COMMENT 'Tag ID'
);

CREATE TABLE `Game_with_Category` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `CategoryID` string NOT NULL COMMENT 'Category ID'
);

CREATE TABLE `Game_with_Platform` (
  `GameID` string PRIMARY KEY NOT NULL COMMENT '遊戲ID',
  `SystemID` string NOT NULL COMMENT 'SystemID'
);

ALTER TABLE `Tem_Transfer` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Cost_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `TopSale_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `HourPlayed_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `MostPlayed_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Steam_Broadcast_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Twitch_by_Date` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Game_with_Tag` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Game_with_Category` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);

ALTER TABLE `Game_with_Platform` ADD FOREIGN KEY (`GameID`) REFERENCES `主機遊戲` (`GameID`);
