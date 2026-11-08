# forensics-tournament-day
This is a (constant work in progress) utility app to use on forensics tournament days to check live-polled competitor times, ranks, and ballot status.


[ ] Unhinged idea: live estimated break probability based on that cume statistically breaking at past tournaments (e.g., for all competitors that got a 6 in round 1, only 21 made an out round (out of 748 total [2.8%]) - 19 champs, one honors, one merit. However, the entry size was 6 (4), 7 (4), or 8 (11) for the 19 champs - the honors break entry was 31 (POE) and the merit was 52 (DI). With entry size in mind, a champs break probability is "0%" and "break at all" probability is ~2/748 (well, 748 minus all of the 6-8 entry events)

^ okay so the way you should do that is just running it through a logistic* regression (or ologit? Break can be binary (1-4 are all "1") or it could be a Champs probability (logit) and break probability (ologit), or a sequence of logits (champs - honors - merit- consi)) that regresses on "Cume after round 1/2/3", entry size, event*, team*** (could also be binary vars for LE/MN/LSW/LSE/etc, if any of those actually add to the model)
