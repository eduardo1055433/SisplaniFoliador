CREATE TABLE `user` (
  `id` smallint(3) UNSIGNED NOT NULL,
  `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `password` char(102) COLLATE utf8_unicode_ci NOT NULL,
  `fullname` varchar(50) COLLATE utf8_unicode_ci NOT NULL
)

INSERT INTO `user` (`id`, `username`, `password`, `fullname`) VALUES
(1, 'OGARCIA', 'pbkdf2:sha256:260000$IikifSl6k7vgo2dq$dd902821e5581a5324e114b22246d25552a0381ed18f83a47512108130971247', 'Oscar Garcia');


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `user`
  MODIFY `id` smallint(3) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

