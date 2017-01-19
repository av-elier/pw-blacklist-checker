import requests
import re
import sys
import uncurl

from name import name

blacklist_items = [
    "curl 'http://concordia-pw.ru/chernyy-spisok/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 YaBrowser/16.11.1.673 Yowser/2.5 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://concordia-pw.ru/forum/forum_2' -H 'Cookie: forum_last=1484669607; dle_user_id=8; dle_password=827ccb0eea8a706c4c34a16891f84e7b; dle_forum_views=%2C3149; PHPSESSID=6760bc8c357d13faa67a7e070b24a615; dle_newpm=0; dle_forum_sessions=6760bc8c357d13faa67a7e070b24a615' -H 'Connection: keep-alive' --compressed",
    "curl 'http://murrclan.ru/viewtopic.php?id=287' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 YaBrowser/16.11.1.673 Yowser/2.5 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: PHPSESSID=a6b235a05311c8d76e23d92ffce4e9c9; incap_ses_450_792128=KjnjWiu0gnyLYg/U5bg+BlFDflgAAAAA77LrxJkkDZJvL8qVeXR8DA==; _ym_uid=1484669777361423729; incap_ses_262_792128=NZ1FegtR63axlP3kwc+iA/9cflgAAAAA1x2ZeA1lrB9pMPJDqc4ouA==; _ym_isad=1; visid_incap_792128=SujvpuDZRZm16v76zG9YcFFDflgAAAAAQkIPAAAAAACAcJJ5ASWT8oOoMvd+TEf39PgyZrrhXHi3; incap_ses_514_792128=wddjSrR5E2ecsB3faRgiBybgf1gAAAAAkNoMmTnQb2iDz5CGTquixA==; _ym_visorc_16138606=w' -H 'Connection: keep-alive' -H 'If-Modified-Since: Wed, 18 Jan 2017 21:37:45 GMT' --compressed",
    "curl 'http://djvega.ucoz.net/forum/2-76-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://djvega.ucoz.net/forum/' -H 'Cookie: edjvegauzfss=lt%3D1484763056%2Cpst%3D1484744795; edjvegaf0=; ucvid=uNmXi2clAe; uSD=-; _ym_uid=1484762733548177730; _ym_isad=1; uSD=4208428900:2778563746; edjvegasocRef=http://djvega.ucoz.net/; edjvegasocses=qckdr8%3BOlWbn%5EVWALCEhsT4x%3BDnnrmrhNH3%3BLrYNyREa2sv3LQcQilYgcPz75PpOwQRqpHqFOcrNxHpARZkDGCeO1D%3B6LH2lrXzDHdyz3%3BOxPA%5EfYgh%3B0eybdcAOSRA0LIjSKgF%3BZpubYJ%3B1zGfDxjqBeLitgNl44vzCuFR%21pfhQAF9wJm8jUdVMhmxnMNzz7K8WbXMgUad6I2tvxWyr3aiTFyZ%21cDxRs9qnCSanNkplt%3Boo; edjvegauzll=1484762906; edjvegauCoz=2r7ANlr8uLyMBvrC; edjvegapPp=0; edjvegap2=0; edjvegapSum=0; edjvegapA16=0' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://the1.ucoz.ru/forum/8-30-1?Zct4GlG' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://the1.ucoz.ru/index/sub/?99-rhsVobfB41-1821185058-http%3A%2F%2Fthe1.ucoz.ru%2Fforum%2F8%2D30%2D1%3FZct4GlG?rdata=QzV4N3puRnBLMCFwRWF0Rk5MVUk1ZFhIaFIxR2s0SVJDQjlYVExUbG1wMUZnZHNuOURBYmRqM1RW%0AVldUcEh3XjJlbkttN2pJcXpnSlghUVg3eVN0YjhpTHM2QmZtZ0NDTkxlQWRCYjJobkxTS0dZSU5L%0ANWluMG1GUGF1NHJJZ1haa2FqeU84UG5jRE80cHBiYlZqMWw7bHg3RmY7MHduekxhRzdeZ0owclRD%0AS2pQZ3dzVnF6emhPc3RlakJOcFExVUdZZHBoeWQyOEdVa1ZZejl4MFphO2ZQWUhhd1dpIUtCa1d2%0AVUVweE5sNUZGS21BTmRXU2p2VzchWDB1bTdWVWNqVlNHNVVGanZQUEN4bVJ0bEtmdFM5R0Frdmoy%0AXnZyO3NxIVUwbWxldTU7QXpVR3FLYlZKUnI2cEZoV2tPUW5SWFY0bEQhVUoxZmVLYnghcV5GTXpL%0AMVJTV0lQeDMhaHQxYlhXWTdiIWZQVW10UEx6WWpweHpyR2h4TlI3eUk4OTZxQUlRbklHUmdQUnlB%0ANlVjYUFkMjRiU1BhMVl5a3huTUo1ZmZFQmxiWTN2a2pSMGxFaHhXYjVmYUdBWGhMTnBPUkZkT1d6%0AcHp1dGNZMG15Rm07TztDYVhpQlJKTnlRMFdlUW5hY0I7ODN4aiFONHdjTFJhU2hjU1JRQWZGO0R1%0AZFpTUWVsN3VORnplekVHNnZoakN6RzI2a2haYzJoMUhJZFI5T3RaN1dTd3pnSG5pempmbHRJVmJa%0AMDRJaEs4WWY1amxzcnZXcHlUVGpCNXJpV152cmZYVTJSY2xScEx1NEc5QThGbw%3D%3D%0A' -H 'Cookie: 0the1uzfss=lt%3D1484763799%2Cpst%3D1484745799; 0the1f0=; ucvid=Tmt6A2uZlR; _ym_uid=1484586362756658855; uSD=2519223650:3378663076; _ym_isad=1; __utmt=1; 0the1socRef=http://the1.ucoz.ru/forum/8-30-1; 0the1socses=2kmHzt4Om9GZQzh2GRxnL%3B4NF3%5Epqv7ZsuhB1WF6DdjLBsm2%21TwzAIdHKOFMxd1p3AaFMDBJyjH%5EisJyju%21CvxS6NwQyKMj5HGNB%5ELNJaz9f815Ni1qZdij8WH2R%21lOJJfkmsK3wh%21BwAaSmKB%5E4JJDlJTkycB2nEyI%21dFkgNgIzphHkcuYzaChk3c%3Bk94Gv1YBZz1ih%21bIcr7HiBehcpSR2GILsZlU43fN8ygzKmrcn9848XIco; 0the1uzll=1484763798; 0the1uCoz=0NUczC5a0QvNMDuV; 0the1pPp=0; 0the1p2=0; 0the1pSum=0; 0the1pA16=0; __utma=126797384.1009847583.1484586361.1484586361.1484763791.2; __utmb=126797384.2.10.1484763791; __utmc=126797384; __utmz=126797384.1484763791.2.2.utmcsr=concordia-pw.ru|utmccn=(referral)|utmcmd=referral|utmcct=/forum/topic_1826' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://assassinpw.clan.su/forum/17-188-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://assassinpw.clan.su/forum/17' -H 'Cookie: 6assassinpwuzfss=lt%3D1484764299%2Cpst%3D1484746274; 6assassinpwf0=; uSD=366854271:1251460025; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; 6assassinpwsocRef=http://assassinpw.clan.su/forum/; 6assassinpwsocses=nh4bO%3BONnd2Wkvg3UQypdj2RVdzM%3BAAjPpxw6nstUHjw7kPEdHQ1kMLmZv3M%3B5va2Y3ptbC73ritJB3i0m%21N53mTiCueIHiPnzqiBxbskmRCvav2MMXQ4U0CXyuP%21xrcg8DE%21WbBt9Bp8Zk%21i04A9VPjZcfaj7fW8daXaLaCw7uyW%21N7VQm6Bwf5cMqILgFyGJviU1WVIWChvQGbBeEAbgqlG%21Rlpt54JQppIxnj7GXDgpx7; 6assassinpwuzll=1484764289; 6assassinpwuCoz=3c9diLlrV8Xf667K; 6assassinpwpPp=0; 6assassinpwp2=0; 6assassinpwpSum=0; 6assassinpwpA16=0' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://cherty.ucoz.ru/forum/19-154-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://cherty.ucoz.ru/forum/19' -H 'Cookie: 0chertyuzfss=lt%3D1484764409%2Cpst%3D1484746398; 0chertyf0=; ucvid=Tmt6A2uZlR; _ym_uid=1484586362756658855; _ym_isad=1; 0chertyuzll=1484764398; uSD=327491147:1288641933' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://dynastypw.ru/viewtopic.php?id=2' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://dynastypw.ru/viewforum.php?id=27' -H 'Cookie: uid=wXx2Olh/tqsyR2I7JOn7AgA=' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://fantasy-clan.ru/viewtopic.php?f=4&t=309' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://fantasy-clan.ru/viewforum.php?f=4&sid=a3cbc853d56627a7b82ec0117365b645' -H 'Cookie: phpbb3_tnpgz_u=1; phpbb3_tnpgz_k=; phpbb3_tnpgz_sid=a3cbc853d56627a7b82ec0117365b645; style_cookie=null' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://guards-pw.ru/viewtopic.php?f=3&t=3' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://guards-pw.ru/viewforum.php?f=3&sid=53eb1accfe32ddec0e12bf4d05010de2' -H 'Cookie: phpbb3_6tlb6_u=1; phpbb3_6tlb6_k=; phpbb3_6tlb6_sid=53eb1accfe32ddec0e12bf4d05010de2; ct_checkjs=16d1904750d4ac597fcea192f815ce6d; ct_timezone=-3; ct_pointer_data=%5B%5B317%2C580%2C1208%5D%2C%5B517%2C580%2C1621%5D%2C%5B717%2C580%2C1821%5D%2C%5B1417%2C580%2C2437%5D%2C%5B2017%2C580%2C2922%5D%2C%5B2617%2C580%2C3361%5D%5D' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://heartlesspw.clan.su/forum/4-521-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://heartlesspw.clan.su/?L47s1Ju' -H 'Cookie: 6heartlesspwuzfss=lt%3D1484765443%2Cpst%3D1484747038; 6heartlesspwf0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; uSD=2682571953:3232681847; 6heartlesspwsocRef=http://heartlesspw.clan.su/; 6heartlesspwsocses=Gsjf%5E7JKdjSZcLC%3BdNcRz6OcZpYXcjasOerJl4BS6YQ7zWCJiCXbMtkaY3DrHG0%3BdSxwTRXC9zpDBsh1OZLw5PMPz4d6ObJlPR372hcj%21z1VsH1zuDzE0auz9FpE%3BmeYJS5OD8OYGitzpOMmTfximeRw5UAR1KMvlf26WceliHZKf%5ETEY2V4DTW%5EKYQI%5ExXun37zmywKmB2K3hDvc%5E7%3BrYtlUZcRctZHUZapWg3JTVaWNfD7sJMo; 6heartlesspwuzll=1484765439; 6heartlesspwuCoz=2QHRqyARWcL6z2ew; 6heartlesspwpPp=0; 6heartlesspwp2=0; 6heartlesspwpSum=0; 6heartlesspwpA16=0' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://indiviso.ucoz.com/forum/12-7-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://indiviso.ucoz.com/forum/?6xdvUIB' -H 'Cookie: dindivisouzfss=lt%3D1484765754%2Cpst%3D1484747710; dindivisof0=; uSD=690699197:1986082939; _ym_uid=1484765707507436751; _ym_isad=1; dindivisosocRef=http://indiviso.ucoz.com/forum/; dindivisosocses=F3UBXfK4DjhJ4ATlKZCdSApKy%3BEaHqSz%3BQlelsCOtKL5xTY4lpRA77e46fmurrWWAYgJGs72L%3Bdl5neVZ0zT9fWkIw2IgtUymu%21fxKanX4DVaudNPVFUrRwpZufGS5H8VXUcPDD1fZ8B88PHE37VMTtJnpPOd1gwkpFYkPl%212yz%5EyzvG%5ElyO1TCzOX9eO7QtFhmuLEpwgMl7p08%3Ba7gDRQ%5E%3B%5E5BT%5E0ylVaW7v1fY2aME0l3V; dindivisouzll=1484765752; dindivisouCoz=0E4aDkTXQgNsRG5i; dindivisopPp=0; dindivisop2=0; dindivisopSum=0; dindivisopA16=0' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://lovestory-pw.ucoz.ru/forum/4-2-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://lovestory-pw.ucoz.ru/forum/4' -H 'Cookie: 0lovestory-pwuzfss=lt%3D1484765942%2Cpst%3D1484747923; 0lovestory-pwf0=; ucvid=Tmt6A2uZlR; _ym_uid=1484586362756658855; _ym_isad=1; uSD=2204802452:3693125202; 0lovestory-pwsocRef=http://lovestory-pw.ucoz.ru/forum/; 0lovestory-pwsocses=HHJmKHbitl6wuKeSNYg%3B7ijRMAtrU34OUv8fIaZ9Vyn%3BzwWcVi10f7ifuHmndx5SlmBHDfjUkRGxp1p5dPmzYHNJbtdVXHXx8St0B%21mtpUe3uc8fWkMz%5E6wCHX7yUku69%21IXVqD%5ENdejLdexOttXaYkveSgjWxyMgCnHYnJWBstf0%5EPledP9slq4F%21vsIR39yPYqxdfif0B%21p67KWS3RWNKQkdGU%5EUPjEh1mj3EtqdQl3RpufgEo; 0lovestory-pwuzll=1484765922; 0lovestory-pwuCoz=3Pro7pok1m6nWs1H; 0lovestory-pwpPp=0; 0lovestory-pwp2=0; 0lovestory-pwpSum=0; 0lovestory-pwpA16=0' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://raiders-pw.clan.su/forum/74-1700-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://raiders-pw.clan.su/forum/74' -H 'Cookie: 6raiders-pwuzfss=lt%3D1484766149%2Cpst%3D1484748134; 6raiders-pwf0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; 6raiders-pwuzll=1484766127; uSD=2812582000:4176386998' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://pw-skystyle.ru/forum/42-16-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://pw-skystyle.ru/forum/42' -H 'Cookie: 0pw-skystyleuzfss=lt%3D1484766387%2Cpst%3D1484748378; 0pw-skystylef0=; _ym_uid=1476040747841566052; 0pw-skystyleuzll=1484766378; uSD=4024284841:2962732399; _ym_isad=1; fa_stylesheet=default' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://sunterra.clan.su/forum/3-27-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://sunterra.clan.su/' -H 'Cookie: 6sunterrauzfss=lt%3D1484766750%2Cpst%3D1484748750; 6sunterraf0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; 6sunterrauzll=1484766712; uSD=448783060:1173741842' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://terraon.clan.su/forum/8-478-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://terraon.clan.su/forum/8' -H 'Cookie: 6terraonuzfss=lt%3D1484766911%2Cpst%3D1484748899; 6terraonf0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; 6terraonuzll=1484766842; uSD=550814109:2141110875' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://pw-vampires.ucoz.com/forum/5-228-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://pw-vampires.ucoz.com/forum/5' -H 'Cookie: dpw-vampiresuzfss=lt%3D1484767046%2Cpst%3D1484749039; dpw-vampiresf0=; _ym_uid=1484765707507436751; _ym_isad=1; dpw-vampiresuzll=1484767028; uSD=2533089061:3383876835; ucvid=WpFTn3ZcSR' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://komu-za-30.clan.su/forum/16-240-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://komu-za-30.clan.su/forum/16' -H 'Cookie: 6komu-za-30uzfss=lt%3D1484767152%2Cpst%3D1484749145; 6komu-za-30f0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; 6komu-za-30uzll=1484767121; uSD=1050259128:1641262462; _ym_visorc_12979546=w' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://mpw.clan.su/forum/23-8-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://mpw.clan.su/forum/23' -H 'Cookie: 6mpwuzfss=lt%3D1484767215%2Cpst%3D1484749206; 6mpwf0=; _ym_uid=1484764276144318736; _ym_isad=1; ucvid=bLMYE3Iguv; _ym_visorc_12979546=w; 6mpwuzll=1484767206; uSD=4095386318:2874188040' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://nyb.ucoz.com/forum/11-14-1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://nyb.ucoz.com/forum/11' -H 'Cookie: dnybuzfss=lt%3D1484767288%2Cpst%3D1484749282; dnybf0=; _ym_uid=1484765707507436751; _ym_isad=1; ucvid=WpFTn3ZcSR; dnybuzll=1484767271; uSD=16328685:1605575723' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    "curl 'http://piter-pw.ucoz.org/index/coslist/0-4' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://piter-pw.ucoz.org/' -H 'Cookie: fpiter-pwuzll=1484767352; uSD=1887239621:792133123; _ym_uid=14847673581069467807; _ym_isad=1' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
]

def main():
    
    for blacklist_item in blacklist_items:
        quoted_url = blacklist_item.split(" ")[1]
        url = quoted_url[1:len(quoted_url)-1]

        curl_py_code = uncurl.parse(blacklist_item)
        resp = eval(curl_py_code)

        if resp.status_code != 200:
            print("    ????ERROR at %s" % (name, url))
        elif name in resp.text:
            print("    !!!!FOUND %s IN BLACKLIST (maybe) %s" % (name, url))
        else:
            print("        not found %s at %s" % (name, url))
        if len(resp.text) < 15000:
            print("            but site is pretty small. Maybe was unable to see black list ")

if __name__ == "__main__":
    main()
