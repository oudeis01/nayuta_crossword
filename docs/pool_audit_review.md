# 풀 전수 감사 결과 (코퍼스 케이스 통계 x 사전 케이스 등재)

판정 원칙: 힌트는 코퍼스 용례로만 판단 (사용자 확정 2026-06-12).
genuine = 소문자, 문중, 경계 정상, 영어 문장, URL 문맥 아님.
사전 = vendor/hunspell en_US (SCOWL 계열, 대소문자 구분).

## A. 제거 권고 4개

general tier, genuine 0건, 사전 소문자 거부 (인명/지명/비단어).

  cisco(30) aries(26) plex(19) ology(10)

## B. 회색 제거 권고 0개

사전 거부 + 총 30회 이상 중 genuine 1~2건(잡음 수준).
genuine 표본을 확인하고 진짜 용례가 보이면 구제 대상.

## C. 판단 필요 4개

사전어인데 코퍼스는 문중 대문자 위주 (wales 류).
사용자 규칙상 제거 대상이나 단어별 확인 필요.

### tron  [general] 총 47 / genuine 0 (0%)
- 분포: trunc 4, allcaps 5, cap 17, hyph 3, urlish 18
- (urlish) Diese neue Arbeit von Ryoji Ikeda ist eine erweiterte Version der audiovisuellen Installation data.tron, bei der jedes einzelne Pixel des visuellen Bildes nach 
- (urlish) September Jungle Imperator (interaktive audiovisuelle Installation) The Sancho Plan in Kooperation mit Ars Electronica Futurelab data.tron [8K enhanced version]

### cote  [general] 총 7 / genuine 0 (0%)
- 분포: trunc 1, cap 6
- (cap) A graduate of the Ecole des Beaux-Arts in France, Ahyi produced several masterpieces in Togo and throughout West Africa, notably in Cote d’Ivoire, Benin, Senega
- (cap) Once the works were authenticated, the family contacted France’s specialist art police who have reportedly already raided Le Guennec’s home on the Cote d’Azur, 

### rials  [general] 총 6 / genuine 0 (0%)
- 분포: trunc 4, cap 2
- (trunc) infrastructural expansion during the Cold War, Feher prioritized the indestructible plasticity of the soft mate- rials that characterize everyday logistics of c
- (trunc) Dry-humored, direct, and imbued with historical, political, and social references, Bonvicini’s art never refrains from establishing a critical connection with t

### terns  [general] 총 5 / genuine 0 (0%)
- 분포: trunc 3, cap 2
- (trunc) To create complex pat­ terns of energy one simply uses one aspect of one simple form to control or alter an aspect of another simple form.
- (trunc) This could mean that certain twists and contours, contortions and extortions, of this enterprise trace the ever so pressing questions about where these forms, f

## D1. 회색지대(사전 거부) 12개

david/john 류: genuine이 있어도 소문자 스타일 표기 잡음일
가능성이 높음. genuine 표본만 훑고 일괄 처분 권장.

### tao  [general] 총 246 / genuine 14 (6%)
- 분포: allcaps 7, capinit 40, cap 183, hyph 1, urlish 1, genuine 14
- (cap) Mobile Assassins Ran Tao / Jenny Chowdhury
- (cap) Within this context of healing, we are very proud to present the art installation ­Technoetic ­Pharmakon as a field of dialectic ­entities: a series of Technoet
- (genuine) Not surprising tao that the shift from a matter-based industria l system was being supplanted by a media-based post­ industria l system in which the engineering
- (genuine) We tao have become sereens, and the interaetivity of men has become the interaetivity of screens.

### cartesian  [general] 총 153 / genuine 6 (4%)
- 분포: trunc 1, capinit 7, cap 139, genuine 6
- (cap) The result will reflect both the complex social interactions of the builders and the contrast between the Cartesian world of pure design and the realities of ma
- (cap) Neither was designed for programming images (despite its name, BASIC is hardly user-friendly), but both had the capacity to produce vector graphics—shapes built
- (genuine) Instead of using x and y coordinates in a cartesian manner, they used gravity as an added value to the method of positioning a single point in 2-dimensional pla
- (genuine) This lecture performance introduces alternative knowledge production beyond the construction of a cartesian body/mind dualism in order to challenge dominant nar

### polaroids  [general] 총 145 / genuine 12 (8%)
- 분포: capinit 5, cap 127, urlish 1, genuine 12
- (cap) There’s a lovely sequence in which he and the cinematographer Ed Lachman take Polaroids of each other.
- (cap) The narratives of the video tapes they made together underline this flirtation, but like the adverts and the Polaroids, convey the possibility that the relation
- (genuine) A crucial aspect of her work is her use of pre- existing images from which she draws inspiration, be it images from newspapers, magazines or films, be it film s
- (genuine) In Annotation, on the other hand, he made a twenty-pages-long virtual photo album with photos degraded by age (polaroids gone red, old faded or stained black an

### arcadia  [general] 총 126 / genuine 11 (9%)
- 분포: capinit 5, cap 109, urlish 1, genuine 11
- (cap) More complex in subject and form,Role Model too, 2013, features two images of boys, one on either face of the work, in front of a barrier disguised as a vaguely
- (cap) Our next stops included the Approach (hosting Simone Subal), Vilma Gold (hosting Neue Alte Brücke), and Emalin (hosting Gregor Staiger), followed by a quick lun
- (genuine) And just as amazing are the similarities with genre films produced by Hollywood, both in the assembly, just less paroxysmal, that with the soundtrack, made up o
- (genuine) In the vertigo of a distorted arcadia, bodies and landscape find the mark of a nature on the point of collapse, letting the gaze wander somewhere in the incompl

### celtic  [general] 총 95 / genuine 6 (6%)
- 분포: allcaps 2, cap 86, hyph 1, genuine 6
- (cap) Bohl’s tapestries and collages were inspired by “the Knot Guy,” a mysterious entity who dedicates his online life to seeking out and shaming bad imitations of g
- (cap) For the Celtic queen raped by the Roman invaders the act of revenge by total sacrifice was necessary, although it had no military or political sense and led dir
- (genuine) Andrea Ummarino: electric guitar Federico Perinelli: electric bass Raphael Schuster: drum kit and electronic pad Valentina Cinquini: electric celtic harp derkle
- (genuine) "To identify ni ne people with terminal access around the planet, each to choose a card in sequence to make up the celtic spread (with my card).

### midwest  [general] 총 80 / genuine 3 (4%)
- 분포: allcaps 1, capinit 3, cap 71, urlish 2, genuine 3
- (cap) Jeremiah Diephuis (US/AT), born in 1976 and grew up in the great arcades of the American Midwest.
- (cap) Most dealers happily noted the abundance of major curators; Midwest institutions were frequently cited as a reason for coming, along with the draw of Chicago-ba
- (genuine) The Japanese and the Germans and the four little dragons are going to come over here and set up factories for building machines in our east coast, midwest and s
- (genuine) Living outdoors in the midwest winters is not a a survivable option for Acheta domesticus (house crickets), but perhaps they still yearn for the pastoral grassl

### savannah  [general] 총 71 / genuine 3 (4%)
- 분포: allcaps 1, cap 66, urlish 1, genuine 3
- (cap) Previously, Seipel served as the interim dean of the School of Art and Design at the Fashion Institute of Technology in New York and as a vice president of the 
- (cap) He comes to the museum from the Savannah College of Art and Design, where he has served as head curator of exhibitions since January 2015, and will take up the 
- (genuine) Right from the outset, however, daoula is the result of a collective activity: in the West African savannah the wild silkworms of the genus 'Anaphe/Epanaphe' se
- (genuine) It settles in the open field and without infrastructures along the banks of the Reno river in the outskirts of Bologna, resting on the sediments between reeds, 

### holm  [general] 총 40 / genuine 3 (8%)
- 분포: trunc 12, capinit 1, cap 24, genuine 3
- (cap) The exhibition will be on view at Stellan Holm 1018 Madison Avenue, Monday–Saturday, 10am–6pm.
- (cap) Erik van der Heeg, Eva-Lotta Holm, and Håkan Nilsson, “Intervju med intendenter (del 4): Pontus Hultén, Kunsthalle Bonn och IHEAP, Paris, Dominans av stjärncura
- (genuine) Jessica Sjöholm Skrubbe (Newcastle upon Tyne: Cambridge Scholars, 2016), 39.
- (genuine) Designed in wood, steel, bricks, or recycled materials, thecabanestake their place in thequadratiof the historical garden, rectangles of grass planted with pine

### doppler  [general] 총 39 / genuine 3 (8%)
- 분포: trunc 3, capinit 3, cap 30, genuine 3
- (cap) In forging such cooperations with industry, Gustav Pomberger (*1949), Professor of Applied Computer Science at Johannes Kepler University (JKU) Linz and head of
- (cap) Auf Initiative des damaligen Leiters des Christian Doppler Institutes für Software Engineering, Gustav Pomberger von der Johannes Kepler Universität Linz (JKU),
- (genuine) But it is also the long delay, the doppler effect of missing each other, and getting together outside of time, even if it’s one at a time.
- (genuine) We will work with the overlap in a way that could be compared to the sound phenomena of a doppler frequency effect, or to the temporal structure of a causal loo

### mana  [general] 총 32 / genuine 3 (9%)
- 분포: trunc 2, allcaps 3, capinit 1, cap 23, genuine 3
- (cap) People read his starting of an Internet Party and close collaboration with the Mana Maori Party as a similar kind of mix of interests behind a supposedly unifie
- (cap) And lack of voting for the Internet Mana Party reflected that, in the recent election.
- (genuine) Oldenburg has this mana touch, too; his art is a ray gun of magical transformation.
- (genuine) The gallery takes its name from the Turkish word mana (concept or meaning in Turkish) and was founded by Mehves Ariburnu in 2011.

### vaseline  [general] 총 31 / genuine 3 (10%)
- 분포: cap 27, urlish 1, genuine 3
- (cap) Shards of colored glass injure the soft surface of a Vaseline landscape, on which colored particles and traces of its fabrication are visible.
- (cap) The specific circumstances of the venue and the light characterize the filigree and lightweight appearance of the sculpture and thus diametrically contradict th
- (genuine) For example, simple glass covered with a thin layer of vaseline and pu t in front of the camera forces a brightly lit spot to emit sparks.
- (genuine) Poet RACHEL RABBIT WHITE is obsessed with vintage uranium vaseline glass.

### ach  [general] 총 15 / genuine 2 (13%)
- 분포: trunc 9, allcaps 1, hyph 2, noneng 1, genuine 2
- (trunc) In the show you will find the most famous wooden spaceship on a Brazilian be- ach, a white fringed boot, a pair of bright lightnings and a character grabbing a 
- (trunc) © Adina Secretan Achæoscillator_Towards Incorporeal Forms of Sensing, Listening and Gaze is an ongoing research and AR/VR immersive installation that uses the n
- (genuine) Another clear aim was to e ncourage Ars Electron ica's inte rnational orientation, while ach ieving local acceptance.
- (genuine) e04 accom­ plished the tasks req uired of him with excel lence a nd is distinguished by his outsta nd­ ing intel lectual a nd ath letic ach ievements.

## D2. 회색지대(사전어) 385개

genuine 희박하나 실존. 채굴 필터가 genuine 우선 수집하므로
유지해도 힌트는 genuine 문장이 1순위가 됨. 표본 확인 후 처분.

### christian  [general] 총 2174 / genuine 3 (0%)
- 분포: trunc 3, allcaps 24, capinit 237, cap 1903, hyph 1, urlish 3, genuine 3
- (cap) With the advent of the modern-secular and bourgeois nation-state in Europe, which displaced from governance the European monarchies and the Church, the narrativ
- (cap) Indigeneity, like national or religious identifications (French, German, American, British, Christian, Muslim, etc.), is a heterogeneous identification.
- (genuine) Mainstream media has produced dozens of famous examples, here we’re looking at a small selection: Arranged like a christian Altar there is the sculpture of two 
- (genuine) At the same time we are reminded of the stained glass windows in christian churches too, which depict the Saints of their specific time.

### miller  [general] 총 984 / genuine 1 (0%)
- 분포: allcaps 10, capinit 167, cap 799, urlish 7, genuine 1
- (cap) This would be the ontic side of psychoanalysis, but, as Jacques-Alain Miller emphasized, this just would not have been the way that Lacan would have set out on.
- (cap) Experts and pioneers like creator of Max and Pure Data, Miller Puckette, bio artist Charlotte Jarvis, intersectional machine learning expert Sarah Ciston, and o
- (genuine) ‘[W]ho would ever have thought of my turning Methodist preacher, that is a preacher on “Method” – but I shall do good, to that art for which I live.’46Constable

### constable  [general] 총 710 / genuine 1 (0%)
- 분포: allcaps 2, capinit 106, cap 601, genuine 1
- (cap) In Leigh’s view, none of Turner’s contemporaries—not even Constable—deserves serious consideration as an artist.
- (cap) Touchy and embittered as a result of his lifelong professional rivalry with Turner, Constable appears only in a single cameo, working on The Opening of Waterloo
- (genuine) The Dutchman shared the building with several other lodgers, including office workers, businessmen and a young police constable and his wife.

### john  [general] 총 6871 / genuine 15 (0%)
- 분포: trunc 4, allcaps 105, capinit 829, cap 5912, urlish 3, noneng 3, genuine 15
- (cap) The ensuing investigations are made both individually and in collaboration with others in the gallery space, notably with John Seth, under the banner of long te
- (cap) (1998), made in collaboration with John Seth, as was Hannah Arendt’s account of work, labour and action.
- (genuine) In its focuses on what happensinside, both spatially and anatomically—“Men never look into the sex of women enough,” one labia minora–loving john attests—House 
- (genuine) “At this moment, the distance between stanley brouwn and marie adams comes to x feet, the distance between stanley brouwn and john adams comes to y feet, and th

### peter  [general] 총 4136 / genuine 10 (0%)
- 분포: trunc 4, allcaps 55, capinit 560, cap 3485, hyph 7, urlish 8, noneng 7, genuine 10
- (cap) Other guest curators Peter Zorn (media artist and co-founder of Werkleitz Media Art Center in Halle) and Sandra B.
- (cap) Peter Kogler / Franz Pomassl CAVE "CAVE" was commissioned by the Ars Electronica Center, and produced collaboratively by Peter Kogler, Franz Pomassl and the Ars
- (genuine) For example, I brought in peter Weibel, who produced his media opera *der künstliche Wille*, the beginning of his long-term ailiation with the festival, irst as
- (genuine) Makeshift oices, secretary Lisa paur and the absorber, peter Weibel, who popped in occasionally with his notes to report on what he had soaked up of late and to

### harry  [general] 총 546 / genuine 1 (0%)
- 분포: allcaps 33, capinit 77, cap 434, hyph 1, genuine 1
- (cap) The Intersection of Art and Interactivity Don Ritter "I sometimes think, Harry, that there are only two eras of importance in the world’s history.
- (cap) It is Hotspur, slain on the field of battle, who speaks the line “O Harry, thou hast robbed me of my youth,” but the words might just as well belong to Falstaff
- (genuine) This led her to agitate for advantage and harry her dealers on both sides of the Atlantic.

### frankfurter  [general] 총 344 / genuine 1 (0%)
- 분포: allcaps 7, capinit 36, cap 298, noneng 2, genuine 1
- (cap) He has since been featured in more than twenty group and solo exhibitions at the National Gallery of Iceland; the Reykjavik Art Museum; Frankfurter Kunstverein,
- (cap) Kracauer, who reviewedTabuin the Frankfurter Zeitung(October 6, 1931) was also critical.
- (genuine) Combined as one, the work conjures the sum of its parts—the smell and taste of a ketchup-covered frankfurter topped with deep-fried crispy onions.

### mars  [general] 총 477 / genuine 3 (1%)
- 분포: trunc 34, allcaps 33, capinit 10, cap 393, urlish 3, noneng 1, genuine 3
- (cap) It is the story of a school trip to Mars that is interrupted by an alien attack.
- (cap) The ESA’s efforts are now focused on exploration of the Sun and the magnetic fields of the Earth, Mars, Saturn and the 67P/C-G comet.
- (genuine) Another crucial idea in Marshall’s work was to paint black figures with ivory black, mars black, and carbon black pigments, rather than pigments and mixtures th
- (genuine) Much of the background includes Prussian blue, probably cerulean blue as well, and the actual range of pigments across the surface is limited to these two blues

### berg  [general] 총 331 / genuine 2 (1%)
- 분포: trunc 91, allcaps 13, capinit 3, cap 217, hyph 1, urlish 4, genuine 2
- (cap) You see far fewer older people here than you do in Berlin’s hip Prenzlauer Berg neighborhood, for instance.
- (cap) Participating artists are Jane Alexander, Wim Botha, Steven Cohen, Churchill Madikida, Mustafa Maluka, Thando Mama, Samson Mudzunga, Jay Pather, Johannes Phokel
- (genuine) In my case, I was impressed by a small but nearby evolution of approaches, of which people with names that included “berg” were contributors.
- (genuine) During this period he was strongly influenced by Schön berg, as he himself admits.

### headlands  [general] 총 131 / genuine 1 (1%)
- 분포: capinit 27, cap 89, urlish 14, genuine 1
- (cap) He is a graduate fellow and affiliated artist at Headlands Center for the Arts (2017-2019) and attended the Skowhegan School of Painting and Sculpture in 2018.
- (cap) She authored The Best Most Useless Dress(Badlands Unlimited, 2014), and has held residencies at the Headlands Center for the Arts, Stanford University and the L
- (genuine) Similarly, the southern and eastern coastline of the British Isles with their sweeping lines are younger meetings of sea and land, whilst the northern and weste

### chow  [general] 총 126 / genuine 1 (1%)
- 분포: allcaps 1, capinit 22, cap 99, hyph 1, urlish 2, genuine 1
- (cap) Officeopens not in Jones & Sunn headquarters but in a hospital room, where the company’s chairman, Ho Chung-ping (Yun-Fat Chow), is at the bedside of his comato
- (cap) The initial candidates were selected by internationally recognized art critics and curators (nominated by each participating institution): Xian Chen, Olivia Cho
- (genuine) It was hours ahead of the deadly attack on a gay nightclub in Orlando, so the multi-gallery dinner proceeded as usual with five hundred, industrial-strength art

### mike  [general] 총 1314 / genuine 12 (1%)
- 분포: allcaps 22, capinit 211, cap 1066, hyph 1, noneng 2, genuine 12
- (cap) , 2001, 16mm), and also seemed set in conversation with Mike Stubbs’s
- (cap) Coordinated Movement · Mike Pelletier Body is personal, body is physical.
- (genuine) By the time organizers convinced the interloper to put down the mike—“It isn’tyourevening”—the point seemed moot.
- (genuine) For example, in David Askevold's FiU, the artist wraps pie ces of foil around a microphone head; as the image (the silver ball offoil) increases, the sound (the

### galleria  [general] 총 1232 / genuine 11 (1%)
- 분포: allcaps 38, capinit 113, cap 1055, hyph 3, urlish 9, noneng 3, genuine 11
- (cap) Frieze Projects is also paying tribute to the Galleria La Tartaruga, an experimental arts space active in Rome during the middle of the twentieth century.
- (cap) Pillole tra industrial design e artediscussants Marco Ponzano (Collezione Branca), Giovanni Perfetti (Galleria Ferrari) Muse Impresa
- (genuine) Raised in the DustatFormer Zoo of Torino In the setting of Parco Michelotti, inside the former Giardino Zoologico di Torino, in collaboration with Città di Tori
- (genuine) The galleria collicaligreggi is pleased to announce the personal show of the artist Alice Cattaneo entitled “Un qui puntiforme unitissimo”.

### lynch  [general] 총 649 / genuine 6 (1%)
- 분포: allcaps 5, capinit 136, cap 501, urlish 1, genuine 6
- (cap) (Lynch’s will, at its most self-serving, makes a world where a mere vicissitude of production can seem like a gotcha, any hole in the plot suggestive of a void.
- (cap) The 1976 adaptation of The Little Girl Who Lives Down the Lanestars a thirteen-year-old Jodie Foster as Rynn and features, in a nude scene, her older sister as 
- (genuine) Once Lovejoy’s character is caught and jailed, this fairly straightforward tale of a man undone by ambition takes on a wider social scope, as a newspaper column
- (genuine) “MAN MOLDED THE DOMESTIC DOGin his own worst image…self-righteous as a lynch mob, servile and vicious, replete with the vilest coprophagic perversions…and what 

### carnivore  [general] 총 97 / genuine 1 (1%)
- 분포: capinit 8, cap 88, genuine 1
- (cap) ), 'They Rule' Futurefarmers, 'Carnivore' of RSG '.
- (cap) ), creator of false home page based on research on the net, the supergroup of RSG with one of the applications software art 'Carnivore', (see
- (genuine) Different from carnivore, omnivore, locavore, vegetarian, or vegan diets, what definesCLIMAVOREis not the ingredients but the infrastructural responses to clima

### nick  [general] 총 744 / genuine 8 (1%)
- 분포: allcaps 19, capinit 115, cap 598, hyph 2, urlish 2, genuine 8
- (cap) Mozilla and The Tech Museum of Innovation Nick Leoni
- (cap) The scenography is created by Nick Verstand and consists of eight robotic arms embracing the musi- For the second part of the concert, the eight cellists are jo
- (genuine) Hopping out of a black cab, a Hamley’s bag in each hand, a raspberry-corduroyed Tal R was in the nick of time for a talk on Armes de Chine , at this location ei
- (genuine) Italian photographer Luigi Ghirri (1943–1992) was once a surveyor, and indeed, his camera combed the landscape like a theodolite, producing pictures that often 

### yahoo  [general] 총 76 / genuine 1 (1%)
- 분포: allcaps 1, capinit 1, cap 64, urlish 9, genuine 1
- (cap) The acquisition by Yahoo in 1999 coincided with a blatantly commercial turning point in the management.
- (cap) This slow decline ended in 2009 with the final closure of the site by Yahoo, leaving all the Geocities archives offline and transforming the busy digital city i
- (genuine) A custom code written in MaxMSPgenerates the soundscape by reading weather related data from yahoo weather; the code modulates different part of the soundscape 

### hopper  [general] 총 279 / genuine 4 (1%)
- 분포: capinit 34, cap 239, hyph 1, urlish 1, genuine 4
- (cap) Florine Stettheimer’s hectic and irrepressible “Cathedrals” paintings, 1929–42, hung within view of Edward Hopper’s noiseless account of the city,From Williamsb
- (cap) Through him, she met artists Edward Hopper, John Sloan, and Marcel Duchamp—on whom she wrote her senior thesis.
- (genuine) “The downside is that they might have to wait for days for the wind hopper to move on and on, and then be able to move for maybe five minutes.
- (genuine) “The downside is that they might have to wait for days for the wind hopper to move on and on, and then be able to move for maybe five minutes.

### macron  [general] 총 68 / genuine 1 (2%)
- 분포: capinit 9, cap 58, genuine 1
- (cap) Since taking office in May 2017, French president Emmanuel Macron has declared that the repatriation of artifacts to Africa would be a “top priority” during his
- (cap) Her bid was supported Hollande—against the counsel of the foreign affairs ministry, according to diplomatic sources—and was also endorsed by his successor, Emma
- (genuine) As for technical solutions, Collections Online makes a point of supporting the macron, a relatively rare diacritical mark that is used extensively in written Ma

### barker  [general] 총 124 / genuine 2 (2%)
- 분포: allcaps 2, capinit 11, cap 109, genuine 2
- (cap) The work of Noah Barker incorporates a distanciated logic in relation to context and intention as a shadow of structural condition.
- (cap) For Fanta, Barker has proposed a publishing pavilion against the idea of a publishing house for the reintro- duction of a text trapped in time.
- (genuine) Prints of the film, which features a former flimflam man and carnival barker elevated to the level of populist demagogue, were rounded up and destroyed when the
- (genuine) As a barker in a brightly painted truck informs us, Abrantes is not only the director of this local ensemble, but an artist keenly attentive to the process of f

### quadrature  [general] 총 116 / genuine 2 (2%)
- 분포: capinit 25, cap 82, hyph 2, urlish 5, genuine 2
- (cap) The emphasis of Quadrature’s works is on the intersection of the physical and digital worlds, of object and code.
- (cap) The three members of Quadrature, Jan Bernstein (DE), Juliane Götz (DE) and Sebastian Neitsch (DE), work and live Berlin.
- (genuine) For example, I designed a radar system hav­ ing both the in-phase and the quadrature components.
- (genuine) The first modulator axis is adjusted for orientation along the Red / Cyan axis, while the second modu­ lator is set 90 degrees in quadrature on the Green / Mage

### packer  [general] 총 58 / genuine 1 (2%)
- 분포: allcaps 2, capinit 5, cap 49, hyph 1, genuine 1
- (cap) Unlike other contemporary artists who claim the portrait as their métier, Packer isn’t aiming to glamorize anyone, much less idealize them.
- (cap) Many critics have noted how closely Packer’s figurative paintings resemble abstract ones.
- (genuine) Schumann has worked with Printed Matter for twenty-six years, beginning as a book packer in 1989.

### sahib  [general] 총 56 / genuine 1 (2%)
- 분포: capinit 9, cap 46, genuine 1
- (cap) Recent teaching staff, guest lecturers and speakers include:Ghislaine Leung,Rosalind Nashashibi,Penny Goring,Rachel Jones,Adam Farah,Chris McCormack,Helen Cammo
- (cap) She curated the ICA’s recent exhibitions of Richard Hamilton, Tauba Auerbach, Hito Steyerl, Prem Sahib, Betty Woodman, and Sonia Boyce.
- (genuine) The white sahib must have had it built for his memsahib.

### tony  [general] 총 977 / genuine 19 (2%)
- 분포: allcaps 18, capinit 112, cap 828, genuine 19
- (cap) I had graduated from Douglass College, the women’s college at Rutgers University, in 1968, and gone on to graduate school at Hunter College in New York City, wh
- (cap) Ashes Don’t Fall Equally © Lorena Cocora ASCEND © Tony Macpela Ashes Don’t Fall Equally explores how ­climate ­justice is hidden behind corporate interests and 
- (genuine) Now that the two shows are siblings, one wonders how much longer the more toned and tony Frieze New York will continue to operate at an inferior site.
- (genuine) Over the ensuing six decades, she designed more than eighty buildings, including private homes, houses of worship, meeting halls, and tony protofeminist headqua

### duff  [general] 총 54 / genuine 1 (2%)
- 분포: capinit 10, cap 43, genuine 1
- (cap) “Crises shake up and clarify things,” artist Arthur Duff noted.
- (cap) Set in Alabama, the film quietly but potently examines the iniquities of racism through their impact on a newlywed couple, Duff (Ivan Dixon), a railroad worker,
- (genuine) Captured in a single 20-minute performance, the film is a recursive compendium of duff chords, anxious grimaces, and phobic uncertainty.

### pom  [general] 총 53 / genuine 1 (2%)
- 분포: allcaps 2, cap 39, hyph 11, genuine 1
- (cap) For my final stop, I visited the studio of artist collective Chim ↑ Pom, located in a prewar house in Koenji, the epicenter of Japan’s punk scene.
- (cap) Artists include Noor Abuarafeh; Asim Abu Shakra; Abbas Akhavan; Farah Al Qasimi; Heba Y Amin; Atelier HOKO; Sophia Balagamwala; Sammy Baloji; Jumana Bayazid El 
- (genuine) Early troupes wore costumes derived from the pierrot character of French pantomime, typically loose pantaloons and tunics with ruffles around the neck, big blac

### deacon  [general] 총 51 / genuine 1 (2%)
- 분포: capinit 6, cap 43, urlish 1, genuine 1
- (cap) Artists:Finn Theuws, Flora Fritz, Greta Eimulytė, Levi van Gelder, Lizzy Deacon, Lorian Gwynn, Ruoru Mou, Sofía Salazar Rosales, Swan Lee, Tumelo Mtimkhulu.
- (cap) With an exhibition space of 1,300 square meters, the foundation not only shows its collection, but also hosts exhibitions by renowned contemporary artists, incl
- (genuine) young and de deacon board, and Honey Pot Performance.Click here for a scheduleof events and programs.

### gee  [general] 총 49 / genuine 1 (2%)
- 분포: capinit 1, cap 44, hyph 3, genuine 1
- (cap) During her tenure at the Whitney, Lampkins-Fielder oversaw programming for the exhibition “The Quilts of Gee’s Bend” (2002–2003).
- (cap) Davis, Matt Donovan, Sean Friar, Colin Gee, Elliott Green, Jiminie Ha, Albertus G.
- (genuine) For me, I just stand there and think,gee whiz.

### hamburger  [general] 총 332 / genuine 7 (2%)
- 분포: allcaps 2, capinit 13, cap 295, hyph 9, urlish 5, noneng 1, genuine 7
- (cap) Hans Hamburger (consultant physicians), Kees Reedijk (programming and electronics), Mondriaan Fund (NL), Rijksakademie (NL), National Culture and Arts Foundatio
- (cap) Schmidt most recently served as a curator at the Hamburger Bahnhof, where she organized the Carl Andre exhibition “Sculpture as Place, 1958–2010,” last May.
- (genuine) There was a picture of a hamburger, and it was a hamburger.
- (genuine) In this new series, the viewers are introduced to unique arrangements of several stalwarts, including fuzzy and plastic figurines of Chewbacca (Star Wars); Cook

### fen  [general] 총 48 / genuine 1 (2%)
- 분포: trunc 36, cap 11, genuine 1
- (trunc) The art historian Clarival do Prado Valladares remarked that from the point of view of the ‘fenômeno brasileiro’ (Brazilian phenomenon) there was no creative re
- (trunc) Die kameraüberwachten städtischen Außenund Innenräume, die Straßen, Kaufund Parkhäuser, Bankfilialen, Bahnhöfe oder Flughäfen sind jedoch keine Einschließungsmi
- (genuine) He also involved himself in his father’s project of draining fen lands – the Lindsey level – in Lincolnshire.

### politico  [general] 총 46 / genuine 1 (2%)
- 분포: trunc 2, cap 4, hyph 38, urlish 1, genuine 1
- (hyph) The term “Global Caribbean” was first used by political scientists such as Robert Buddan to describe the globalized, borderless Caribbean politico-economic sphe
- (hyph) The work is a politico-philosophical conceptualisation of “The New” – a term which reverberates not only across consumer society but the world of art as well.
- (genuine) The first side of the original LP uses surreal poetry by Benge as its lyrical source, but the flip finds Wyatt stuck in politico mode (and sounding as if it’s w

### whiting  [general] 총 46 / genuine 1 (2%)
- 분포: allcaps 2, capinit 7, cap 36, genuine 1
- (cap) A report commissioned by the board of the Mexican Museum in San Francisco has concluded that almost all the artifacts from the institution’s pre-Hispanic collec
- (cap) Over the weekend of March 7 and March 8, friends and family of artist Susan O’Malley completed a hand-lettered mural along San Pablo Avenue in Berkeley, reports
- (genuine) WHITEOUT also refers to Thomas Wachholz’ technique of whiting out the color on the canvas with ethanol.

### lamas  [general] 총 43 / genuine 1 (2%)
- 분포: capinit 5, cap 36, urlish 1, genuine 1
- (cap) Through the works of Olga Balema, Eli Cortiñas, June Crespo, Mario Espliego, Antoni Hervàs, Salomé Lamas, Anna MorenoandBruno Pacheco, the exhibition affords un
- (cap) Salomé Lamas: Screening and Discussion
- (genuine) Staged at the Nicola Trussardi Foundation, Milan, in 2006, it brought together goats, dogs, ducks, chickens, horses, lamas, cows, peacocks, ponies, turkeys, she

### manna  [general] 총 205 / genuine 5 (2%)
- 분포: allcaps 1, capinit 24, cap 174, urlish 1, genuine 5
- (cap) CRG Gallery Booth B26Tonico Lemos Auad / Steven Bindernagel / Alexandre da Cunha / Tomory Dodge / Pia Fries / Ori Gersht / Joana Hadjithomas and Khalil Joreige 
- (cap) Sculpture Center is pleased to announce the simultaneous presentations of new work by four artists, Rossella Biscotti, David Douard, Radamés “Juni” Figueroa, an
- (genuine) The sculptural project is a radical reading of the legend of the manna, the miraculous bread the hebrews ate in the desert while running from slavery in Egypt, 
- (genuine) It must have seemed like manna from heaven to a group searching for a new.

### kohl  [general] 총 42 / genuine 1 (2%)
- 분포: allcaps 2, capinit 2, cap 32, hyph 5, genuine 1
- (cap) She will assume her full duties in early September.“Over several years, I have come to know Andria as a contemporary curator of the highest order and as one who
- (cap) Among the other members of the board are Andrea Bowers, John Geresi, Karyn Kohl, Rodney McMillian, and Mary Weatherford.
- (genuine) The image recalls stop-motion photography (think of Man Ray’s 1922 portrait of the spectacularly eccentric Marchesa Casati, with her wild, doubled eyes drawn in

### rapids  [general] 총 42 / genuine 1 (2%)
- 분포: cap 38, urlish 3, genuine 1
- (cap) Embracing this idea has enabled to grow as an institution and to better serve our community.” The other museums recognized this year were the Boston Children’s 
- (cap) Frederik Meijer Gardens and Sculpture Park in Grand Rapids is inaugurating its twenty-two-million-dollar eight-acre Japanese garden after years of construction,
- (genuine) Violent tribal disputes and unpredictable weather hinder the shoot, but the biggest obstacle is Herzog’s own quixotic and dangerous determination to film one an

### yang  [general] 총 753 / genuine 20 (3%)
- 분포: allcaps 9, capinit 73, cap 633, hyph 9, urlish 9, genuine 20
- (cap) explorations of rural landscapes such as a study of the Pacific Ocean by Minyong Yang (
- (cap) Seoul Li DARs —Hyun Parke (KR/US), Jinoon Choi (KR), Sookyun Yang (KR) Volumetric Data Collector Nathalie Regard (FR/MX), Guillaume Dumas (FR), Roberto Toro (FR
- (genuine) Yin yang, animus and anima, androgyny…poetics of the conjunction whose horizon is liberty.
- (genuine) Another example is the yin and yang circle, in which the white part has a black dot and a the black part has a white dot.

### coco  [general] 총 150 / genuine 4 (3%)
- 분포: trunc 1, allcaps 10, capinit 10, cap 124, hyph 1, genuine 4
- (cap) (You can read details about the events leading up to her arrest and those of other activists on this site’snews columnand in adetailed postby artist Coco Fusco,
- (cap) After winning the Milan Gold Cup at twenty-six, however, he began to cast about looking for more worlds to conquer and landed on cinema, working as an assistant
- (genuine) Coco Fesse also known as coco de mer, love nut or double coconut belongs to an endangered species of palm trees found in the Seychelles.
- (genuine) Evolutions of the redwood, the coco palm and the breadfruit challenge sculptors; there are at least forty varieties of the one, twenty of the other.

### lopes  [general] 총 73 / genuine 2 (3%)
- 분포: trunc 1, capinit 12, cap 57, noneng 1, genuine 2
- (cap) Pedro Lopes from the Hasso Plattner Institut in Germany creates muscle interfaces that read and write to the human body.
- (cap) By realising this work at the twelfth São Paulo Biennial, Lopes had hoped to ‘bring to light’ the work of Grupum, a theatre group she created when she joined UE
- (genuine) While the conventional view of aesthetic experiment imagines the avant-garde artist as an athletic prodigy, leaving an audience choking in the dust at his heels
- (genuine) It seems like Jim can’t either; when the shadow lopes off to the bathroom, he asks, “Should I really kill him?” The sound of a toilet flushing gives way to a ch

### fortes  [general] 총 37 / genuine 1 (3%)
- 분포: capinit 3, cap 31, hyph 1, urlish 1, genuine 1
- (cap) at Galeria Fortes Filaça, São Paulo, Brasil until 14 September 2013 .
- (cap) Courtesy of Galeria Fortes Filaça, São Paulo, Brasil
- (genuine) Despite having a broken finger, Atoui played nonstop in a frenzy of physical activity, balancing pianissimi with fortes while stabilizing the scaffolding that s

### aster  [general] 총 35 / genuine 1 (3%)
- 분포: trunc 1, allcaps 13, cap 18, urlish 2, genuine 1
- (cap) Robdilo’clock Benjamin Aster
- (cap) Benjamin Aster’s Plottegoino testifies to his innovative spirit and great enthusiasm for tinkering and for handicrafts with his marvelous little plotter that tr
- (genuine) It suggests that the site of Alves’s project might have been home to red maples, American hornbeam, starved panic grass, prairie fleabane, and white wood aster,

### digitalis  [general] 총 34 / genuine 1 (3%)
- 분포: allcaps 7, cap 24, urlish 2, genuine 1
- (cap) © Marcel Bückner Communication Design, School of Culture and Design, University of Applied Sciences Berlin (DE) Emanatio Digitalis Emanatio Digitalis questions 
- (cap) © Marcel Bückner Communication Design, School of Culture and Design, University of Applied Sciences Berlin (DE) Emanatio Digitalis Emanatio Digitalis questions 
- (genuine) They have been selected from dialogues generated by the project Agora Phobia (digitalis).

### dong  [general] 총 203 / genuine 6 (3%)
- 분포: capinit 4, cap 147, hyph 45, urlish 1, genuine 6
- (cap) Ding Dong If you enjoy experimenting with tones and sounds, then join us as we bring sound to our house on non-instruments.
- (cap) She was the first curator in the United States to showcase the work of Asian artists Zhang Peili, Song Dong, Teiji Furuhashi, Feng Mengbo, and Yang Fudong.
- (genuine) Ore for them, molten slag for the rest of us.Ding dong, tomorrow still belongs to her.
- (genuine) Above – Old weather , 2015 Tilia Americana , 2014 Ding dong in the mirror , 2015 Okie Dog on Santa Monica , 2015 Okie Dog on Santa Monica (detail), 2015 Old wea

### starling  [general] 총 134 / genuine 4 (3%)
- 분포: allcaps 1, capinit 9, cap 120, genuine 4
- (cap) Simon Starling interviewed by Eva Fabbris Eva Fabbris Among the works featured in your show at the Modern Institute, there are new daguerreotypes that are part 
- (cap) Simon Starling It’s a building I’d seen a lot of images of, but somehow until you actually go there you don’t really understand the place.
- (genuine) A work is hanging on the wall above it: a star-shaped cross made out of starling cadavers.
- (genuine) In intimate work in progress sessions, the artists will dance, explain and show the upcoming work based on the storyboard and the musical score, enriched by int

### comer  [general] 총 132 / genuine 4 (3%)
- 분포: trunc 19, allcaps 6, capinit 3, cap 96, hyph 3, noneng 1, genuine 4
- (cap) They included a heavy complement of curatorial power—Hans Ulrich Obrist, Stuart Comer, the Walker’s Fionn Meade and Pavel Pyś, Tom McDonough, Tom Eccles, Chriss
- (cap) The Museum of Modern Art, New York, has appointed Stuart Comer as chief curator of its department of media and performance art.
- (genuine) As she does so, Abigail becomes a mouthpiece for the opposition Tories, looking to check the Whiggish duchess, and is cultivated for this job by Robert Harley, 
- (genuine) Somehow I' d gotten the idea that some oj the serious music composers consider the Moog a late comer that is not totally welcome.

### jack  [general] 총 1168 / genuine 37 (3%)
- 분포: allcaps 14, capinit 137, cap 960, hyph 18, urlish 2, genuine 37
- (cap) Using the Eye Jack Augmented Reality App, you can see the front page of the New York Times come to life with animation and sound as the stories are deconstructe
- (cap) In this context the Eye Jack app allows the user to perform a news autopsy—a post-print examination that explores the climate of events surrounding the news sto
- (genuine) In the diary he kept (and published) on Full Metal Jacket, Modine goes from calling Vitali a “jack of all trades” to a “slave.” “Answering everything that came 
- (genuine) We are thoroughly acquainted with these spaces, these corporate settings and tokens of urban planning, chopped and screwed out of context and locality, scattere

### goldsmith  [general] 총 154 / genuine 5 (3%)
- 분포: allcaps 1, capinit 17, cap 131, genuine 5
- (cap) Sebald and an abhorrence of nonsocialized health care, Parrish director Terrie Sultan announced that Close, along with director-choreographer Patricia Birch, ch
- (cap) Musing on the range of reactions provoked by their forthcoming project, cocurator Gil Goldsmith said: “It is a very fragile situation and there are, as you can 
- (genuine) Our family name, at that time, was Sayegh(which means goldsmith).
- (genuine) Crafted by Russian goldsmith Peter Carl Fabergé and his workshops, these eggs commemorated and worshipped the history of the Russian empire as well as technolog

### gander  [general] 총 211 / genuine 7 (3%)
- 분포: allcaps 3, capinit 16, cap 185, genuine 7
- (cap) We could ask the same of Danh Vo, Ryan Gander, Grace Ndiritu, or Kai Althoff, some of whom are embarking on ambitious real estate projects, refurbishing barns o
- (cap) For these artists—whether Ndiritu, or Danh Vo in a farmhouse in Brandenburg, or Andrea Zittel in her long-term living-working project in Joshua Tree, or Ryan Ga
- (genuine) Socialite vixen Paris Hilton is in the driving seat, in the wrong pozzie to get a gander at plucked Chicken Little, Henny’s pretty pennies.
- (genuine) Musicians including the Band’s Robbie Robertson and the venerable Van Dyke Parks took a gander too.

### tat  [general] 총 91 / genuine 3 (3%)
- 분포: trunc 64, allcaps 1, cap 12, hyph 8, urlish 1, noneng 2, genuine 3
- (trunc) the first time as tragedy, the second as farce.” Thus begins The 18 th Brumaire , his book about the coup d’état led by the French president-turned-emperor, Lou
- (trunc) Patricio Guzmán’sThe Battle of Chile (Part 2): The Coup D’Etat(1976), which was screened at the end of the event, closely studied the political developments imm
- (genuine) The Chilean military coup d’état of 11 September 1973 unseated the democratically elected socialist government of Salvador Allende.
- (genuine) This ‘tit for tat’ strategy makes the spectator feel uncomfortable but also empowered.

### mambo  [general] 총 90 / genuine 3 (3%)
- 분포: allcaps 23, capinit 2, cap 61, hyph 1, genuine 3
- (cap) At the evening’s end, after an appeal raised more than $120,000 in under fifteen minutes, after all the songs and tributes and stories, Kevin Mambo took the sta
- (cap) The Premio Furlaaward, conceived by Chiara Bertola, is now organised and promoted by Fondazione Furla, Fondazione Querini Stampalia, MAMbo – Museo d’Arte Modern
- (genuine) There wasn’t anything like that before – all you could do was go to a cocktail bar that had a little piece of floor for the mambo or the twist.
- (genuine) Whereas most free-jazz players came to the music through bebop, Graves arrived via Latin music, to which he was introduced by a popular radio show during the ma

### lye  [general] 총 61 / genuine 2 (3%)
- 분포: capinit 10, cap 49, genuine 2
- (cap) For her 2012 video No Lye —in which bathroom beauty chitchat turns into guidelines for making a bomb—she perused sixty years of back issues of the black US maga
- (cap) Smith, Sidsel Meineche Hansen, Liz Magor, Len Lye, Marguerite Humeau, Dirk Braeckman, Wu Tsang, Nora Turato, Emily Mae Smith, Luke Ching Chin WaiLiquefied Sunsh
- (genuine) Exogenous substances are integrated: lye, softener.
- (genuine) Look at that pile of cinders on the left they call as dune, the gray dam to our right, the bluish beach at our feet, the sea the color of pale lye in front of u

### cirque  [general] 총 30 / genuine 1 (3%)
- 분포: allcaps 1, capinit 1, cap 26, noneng 1, genuine 1
- (cap) He has worked as a choreographer and director on numerous projects, including the Cirque du Soleil’s Varekai, Opéra de Montréal`s Carmina Burana, a theatrical w
- (cap) This work is inspired by Miss La La at the Cirque Fernando , an 1879 masterpiece by Edgar Degas, which shows an acrobat in a daring perspective from below.
- (genuine) Wiangthong’s voguing cirque thus doubled as a mocking critique of contemporary power paradigms that enervate the bodies of workers.

### krone  [general] 총 30 / genuine 1 (3%)
- 분포: allcaps 9, cap 19, hyph 1, genuine 1
- (cap) Money in Friends With August Diehl, Tanja Krone, Marc Limpach, Julia Malik and Hans Narva from “Maiden Monsters” and “Hands up – Excitement!” — — SALON POPULAIR
- (cap) Before putting down my pen and surrendering to the nearly two-hour long bacchanal, I counted four different ensembles (courtesy of Larry Krone/House of Larréon)
- (genuine) We skipped stones wearing only our blue knickers from a one Danish krone store, galloped into crooked cartwheels and short-lived handstands, spread our arms wid

### lees  [general] 총 30 / genuine 1 (3%)
- 분포: capinit 2, cap 27, genuine 1
- (cap) The Aspen Art Museum (AAM) in Colorado announced today that Nicola Lees has been appointed its next director.
- (cap) Prior to joining New York University, Lees was head of the Frieze Foundation from 2013 to 2015 and curated Frieze Projects London, mounting over forty large-sca
- (genuine) Now and then, dust devils and avalanches appear, as do lees where lightweight particles seem to dance over a solid surface.

### hertz  [general] 총 117 / genuine 4 (3%)
- 분포: allcaps 1, capinit 5, cap 103, urlish 4, genuine 4
- (cap) A prominent role in this turning-point, whose significance is probably equalled only by the invention of writing 60, was taken by Maxwell’s electromagnetic fiel
- (cap) Since 2003 he is head of the Institute for Music and Acoustics at ZKM|Karlsruhe, now Hertz-Labor, and guest professor at the School of Design.
- (genuine) Among them is 432 hertz, which harmonizes the patterns of our bodies, and 852 hertz, hailed as a conduit back to the spiritual order.
- (genuine) Among them is 432 hertz, which harmonizes the patterns of our bodies, and 852 hertz, hailed as a conduit back to the spiritual order.

### blooded  [general] 총 29 / genuine 1 (3%)
- 분포: hyph 28, genuine 1
- (hyph) In this hot-blooded prison drama, director Jacques Audiard builds scenes of queasy intensity and then fits them into a skillfully concocted, near-epic framework
- (hyph) He claimed a privileged understanding of an older, more red-blooded and socially necessary artistic tradition.
- (genuine) The blanched gorgeousness of their outfits, blooded by the hot royal red of the christening gowns, was part of it.

### dill  [general] 총 29 / genuine 1 (3%)
- 분포: capinit 11, cap 17, genuine 1
- (cap) By Lucie Riley—The subtitle of Lesley Dill’s new exhibition of sculptures and painted banners, “Until the Urge to Rise Meets the Urge to Fall”comes from poet To
- (cap) How it acts on us.” (Thryza Goodeve) Dill's art has long made its place at the interface of image and poetic text drawn from a select group of poets and writers
- (genuine) In her latest show Mange d’haleine at gr_und, Berlin (2022), the space was divided in two by a plastic curtain, giving it a forensic feel, and there was fresh d

### lien  [general] 총 112 / genuine 4 (4%)
- 분포: trunc 58, capinit 7, cap 42, urlish 1, genuine 4
- (trunc) Aurélien Le Genissel is an art critic and independent curator based in Barcelona and Paris.
- (trunc) Aurélien Le Genissel is an art critic and independent curator based in Barcelona and Paris.
- (genuine) Aurélien Mole “Bénin” Aure?lien Mole cultivates a dandy artist approach, combining sophistication precision and poetic of the making.
- (genuine) Pursuing Bayard’s experiments, Aure?lien Mole studies and plays with the conditions of appearance of things, with their tangibility in representation and produc

### legged  [general] 총 110 / genuine 4 (4%)
- 분포: capinit 2, cap 8, hyph 96, genuine 4
- (hyph) The course for advanced users involves teaching a six-legged hexapod to walk, and, in doing so, getting an introduction to the field of bionics.
- (hyph) Indeed, Murnau did sweeten the nocturnal scenes with an outsize artificial moon—and, as Eisner disapprovingly noted, the “odd, short-legged Inselmädchen[island 
- (genuine) function, CIVC robots have evolved from simple wheeled devices to some recent legged forms with astonishing adaptability (and more than just a passing biologica
- (genuine) RoboLab Hexapods In contrast to the two legged Plens the Hexapods show that 6 legs are much better for robots.

### tosh  [general] 총 28 / genuine 1 (4%)
- 분포: trunc 1, capinit 1, cap 24, urlish 1, genuine 1
- (cap) The stage—featuring a microphone, screen, and many empty beer cans—displays framed portraits of comedians famous for misogyny or for accusations of sexual assau
- (cap) The film, interpreted by performers Rocío Molina with José “El Oruco,” Yinka Esi Graves, Tosh Basco and the bullfighter Vanessa Montoya, utilizes multi-channel 
- (genuine) John Russell writing in the Sunday Timesaccepted the ‘individual power’ of Jackson Pollock’sOcean Greyness1953 but wrote that ‘the Franz Kline, the Stuart Davis

### trump  [general] 총 957 / genuine 35 (4%)
- 분포: allcaps 9, capinit 68, cap 844, hyph 1, genuine 35
- (cap) On the one hand, the appalling rise of xenophobia and racism in Europe and the United States in the wake of divisive populist politics (read Trump, Brexit, etc.
- (cap) Following the recent data-mining scandal involving Facebook and a political firm that provided user information to Donald Trump’s presidential campaign, the Tur
- (genuine) Yet there are times when all this creativity betrays a manic energy—I can’t help myself!—as well as an aggressive defiance:I can trump anyone!
- (genuine) When the gallery of the artist’s Paris dealer Camille Goemans collapsed in 1930, Mesens came to the rescue, buying up a batch of eleven works – a feat he was to

### passers  [general] 총 190 / genuine 7 (4%)
- 분포: capinit 11, cap 1, hyph 170, urlish 1, genuine 7
- (hyph) On several evenings during the Ars Electronica Festival, after the sun has set, different audiovisual projects are projected onto the media facade, inviting fes
- (hyph) Via multimodal interfaces, the facility’s transparent architecture is opened up to interaction with employee/users as well as passers-by.
- (genuine) Sometimes, as in another scene that was played out recently on a tiny square on the outskirts of Vienna, a WLAN user simply lets his park-bench neighbor and mor
- (genuine) In addition, passers by on the Lower East Side can view The Digital Revolutionaries – The Shiboogi Versionprogram on the Salon 94Bowery video wall, next to the 

### verger  [general] 총 27 / genuine 1 (4%)
- 분포: trunc 9, capinit 4, cap 13, genuine 1
- (cap) Portikus is pleased to announce Städelschule professor Willem de Rooij’s exhibition Pierre Verger in Suriname, on view until July 18, 2021.
- (cap) The core of the installation Pierre Verger in Surinameis a suite of 257 images that were made by French photographer and ethnologist Pierre Verger (1902, Paris 
- (genuine) Having advertised his volume on Salisbury, he discovered that the verger of the cathedral and author of its guidebook, William Dosdworth, had decided to produce

### woo  [general] 총 105 / genuine 4 (4%)
- 분포: capinit 11, cap 71, hyph 19, genuine 4
- (cap) It features younger artists active in the post-internet era since the 2010s, including Don Sunpil, Chu Mirim, Noh Sangho, Sim Raejung, Sungsil Ryu, and Jeongsu 
- (cap) Participating artists:Chu Mirim, Don Sunpil, Jeongsu Woo, Kim Shinhye, Kyoung Tack Hong, MeeNa Park, Noh Sangho, Sim Raejung, Son Donghyun, Sungsil Ryu
- (genuine) When the male sees a female, he makes a little arrangement to impress her, to woo her.
- (genuine) Anyway really it was a double prophylactic and I don’t remember how young I was when I started wearing it: body condom one, to parry the propensity of older men

### bullock  [general] 총 26 / genuine 1 (4%)
- 분포: capinit 1, cap 24, genuine 1
- (cap) at Belmacz Gallery, London until 16 April 2016 Helen Bullock, Untitled , 2016 Helen Bullock, Untitled , 2016 Paul Housley, Head of an English Iconoclast , 2016 
- (cap) at Belmacz Gallery, London until 16 April 2016 Helen Bullock, Untitled , 2016 Helen Bullock, Untitled , 2016 Paul Housley, Head of an English Iconoclast , 2016 
- (genuine) On the same wall in the exhibition, directly below is a photograph of two New Guinean men, working in a copra plantation with an imported Asian bullock pulling 

### mailer  [general] 총 76 / genuine 3 (4%)
- 분포: capinit 4, cap 67, hyph 1, urlish 1, genuine 3
- (cap) Rosset’s name is dropped in several pieces; Norman Mailer and Dotson Rader (perhaps the only SDS member with entrée to the back room at Max’s Kansas City) both 
- (cap) Lita Eliscu, a columnist and rock critic for the biweekly East Village Otherand one of Evergreen’s few hippie types, pondered Godard’sLa Chinoise, Robert Kramer
- (genuine) I first encountered Al-Maria’s work by chance on July 25, 2015, when I idly opened an e-flux mailer only to discover an intriguing post for “Supercommunity,” a 
- (genuine) This piece is about the economic isolation and exploitation of Africa”); script pages (at one point during the project, GALA began to receive advance teleplays 

### sir  [general] 총 498 / genuine 20 (4%)
- 분포: trunc 37, allcaps 3, capinit 63, cap 365, urlish 10, genuine 20
- (cap) From that power base, he shaped a legacy that suggests the epitaph on the tomb of Sir Christopher Wren, who is buried in his masterpiece, St.
- (cap) And though there is little biographical evidence to suggest that when Welles beganChimes at Midnighthe believed, per Dietrich, that his future was already “all 
- (genuine) What about you, sir, in the yellow?”
- (genuine) My memory, sir, is like a rubbish heap.”] Given their historical significance, Pliny’s stories are of undeniable value.

### cockatoo  [general] 총 25 / genuine 1 (4%)
- 분포: allcaps 1, capinit 2, cap 19, urlish 2, genuine 1
- (cap) At a former industrial shipyard on Cockatoo Island, Ai Weiwei’s installation Law of the Journey, 2017, appears predestined for such an effect.
- (cap) That is, in Cut-Out Pollock achieved figuration by negating part of the painted field—by taking something away from it—rather than by adding something as in Whi
- (genuine) Moreover, in the Pasta dossier he stamped the words ‘PASTA’S PARROT’ on a small manila envelope that was stapled onto an image of a white cockatoo (a cover of t

### lech  [general] 총 25 / genuine 1 (4%)
- 분포: capinit 5, cap 19, genuine 1
- (cap) IP Group (PL): Jakub Lech, Bogumił Misala, Dominika Kluszczyk & Ania Haudek LUMEN © Jakub Lech
- (cap) IP Group (PL): Jakub Lech, Bogumił Misala, Dominika Kluszczyk & Ania Haudek LUMEN © Jakub Lech
- (genuine) This side emerges in full view somewhere around the time when Eastwood’s character retires for the first of the movie’s two threesomes, the famous unreformed ol

### ordinates  [general] 총 25 / genuine 1 (4%)
- 분포: hyph 24, genuine 1
- (hyph) The control on the flow of signals that surround us and through the co-ordinates of our body is increasingly complex and elusive.
- (hyph) First, you need to set the texture co-ordinates of each vertex in the Tri Mesh.
- (genuine) The financial curves and graphs of the previous series have lost their abscissa and ordinates, and language is nominally summoned to say nothing.

### gasworks  [general] 총 221 / genuine 9 (4%)
- 분포: capinit 37, cap 156, urlish 19, genuine 9
- (cap) Among those present were artist Minjung Kim, Art India president Sangita Jindal, Alessio Antoniolli from Gasworks, and archeologist Agnes Hsu-Tang (who is also 
- (cap) In a portrait-lined parlor upstairs, Gasworks’ Alessio Antoniolli caught up with Serpentine curators Amal Khalaf and Rebecca Lewin and artists Cécile B.
- (genuine) Last September, the event—which has occupied a former gasworks factory every September for the last eight years—welcomed more than 25,000 visitors and featured 
- (genuine) Patrick McGrathYes, the gasworks worked well.

### watts  [general] 총 264 / genuine 11 (4%)
- 분포: allcaps 1, capinit 22, cap 226, hyph 2, urlish 2, genuine 11
- (cap) I studied with Geoff Hendricks and Bob Watts, to name a few.
- (cap) He played with bassist Jack Bruce in R&B outfits Blues Incorporated (replacing Charlie Watts) and the Graham Bond Organization, beginning a combustible relation
- (genuine) The costs lie mainly in electricity to support the hundreds of watts necesary to reach any great distance.
- (genuine) Because it uses so little energy, the website can be run on a mini-computer which needs only 1-2 watts of power, which is supplied by a small solar installation

### caucus  [general] 총 24 / genuine 1 (4%)
- 분포: cap 21, urlish 2, genuine 1
- (cap) Stewart is the author of Migrating to the Movies: Cinema and Black Urban Modernity, which has achieved recognition from the Society for Cinema and Media Studies
- (cap) Representative Leonard Lance (R-NJ), who is cochairman of the Congressional Arts Caucus, said that as he tries to drum up support for the arts endowments among 
- (genuine) We were thinking about forming a caucus with another organisation, but we soon decided that we needed to be independent.

### lowlands  [general] 총 24 / genuine 1 (4%)
- 분포: capinit 1, cap 19, urlish 3, genuine 1
- (cap) Kingma’s work has also been shown at the Rijksmuseum Twenthe, Museum Flehite, and Lowlands Festival.
- (cap) So far the AR Art exposition Me at the museumplein(spring/summer 2010) and the Stedelijk ARthotequeat popfestival Lowlands (August 2010) and Picnic 2010 (Septem
- (genuine) Here, the flourish of organic line and form, the apparent rests and shifts of bovine breath and muscle seen in the bull, are just as expansive in Johnstone’s ca

### crumb  [general] 총 94 / genuine 4 (4%)
- 분포: allcaps 10, capinit 18, cap 60, hyph 2, genuine 4
- (cap) Two ladies chatting in front of Crumb’s immaculate Mystic Funnies No.1: Mr.
- (cap) A handful are still schlepping around, crates of dusty 78s in tow.Filmdirector Terry Zwigoff is one, as is his friend and the subject of his best film (and one 
- (genuine) UNFINISHED LIST brings together five existing mailing lists (nettime, crumb, faces, -empyre-, spectre) live on radio FRO.
- (genuine) UNFINISHED LIST brings together five existing mailing lists (nettime, crumb, faces, -empyre-, spectre) live on radio FRO.

### signer  [general] 총 94 / genuine 4 (4%)
- 분포: trunc 2, allcaps 2, capinit 14, cap 70, hyph 2, genuine 4
- (cap) By introducing the notion of duration into their conception, Roman Signer broadens the classical definition of a sculpture.
- (cap) Like the phenomena that suddenly modify a given situation or environment, Roman Signer’s works have a sense of tragedy and disaster.
- (genuine) Here he presents a stereoscopic video that offers a very specific choreography, while a signer for deaf persons recreates the movements of the dancer.
- (genuine) “I’m really thrilled that [the judge is] taking it seriously,” said Evelyn Yaari, a petition signer and member of Friends of the Barnes Foundation.

### grosser  [general] 총 46 / genuine 2 (4%)
- 분포: capinit 4, cap 39, urlish 1, genuine 2
- (cap) Thomson’s lover, Maurice Grosser, fashioned the text into a series of tableaux.
- (cap) Ben Grosser – Touching Software
- (genuine) The longer you’re dead, the grosser it becomes that I own everything—your savings, your 401K, your social security benefits, your ashes.
- (genuine) Such contradictions become stereotypes in their own right when, outside the manga panel, the racialized imaginary of Japanese sexuality become an entrenched nar

### yuan  [general] 총 201 / genuine 9 (4%)
- 분포: trunc 2, allcaps 4, capinit 7, cap 175, hyph 2, urlish 1, noneng 1, genuine 9
- (cap) SMB13 X Frieze Film Seoul 2025:Amit Dutta, Angela Su, Anocha Suwichakornpong, Colectivo Los Ingrávidos, Hsu Chia-Wei, Jane Jin Kaisen, Joachim Koester, Karrabin
- (cap) Chen Ching-Yuan first turned to this classical genre as a black hole of meaning, as a way of thinking through the complex turns of colonialism, postcolonialism,
- (genuine) Each stand sprouts 5 diagonal strings which correspond to 5 currencies (US dollar, yuan, euro, Canadian dollar, and Russian ruble).
- (genuine) I remember the book I liked the most, which was on Giacometti, cost 900 yuan back then.

### footed  [general] 총 44 / genuine 2 (4%)
- 분포: cap 1, hyph 41, genuine 2
- (hyph) As he would have said, in his peculiarly flat-footed and practical way, this is probably because he was Venetian.
- (hyph) Craig Garrett grapples with Collier Schorr on the eve of significant exhibitions of her work in New York and London; Giovanni Carmine manages to track down the 
- (genuine) I also footed it downstairs to see salacious drawings by Tom Wesselmann, whose female objects of desire were also objectified in a show at Gagosian Davies Stree
- (genuine) Finally came a closing disclaimer, which revealed, unsurprisingly, that it was Burden who had footed the bill.

### mapper  [general] 총 22 / genuine 1 (4%)
- 분포: cap 21, genuine 1
- (cap) Software: open Frameworks, Mad Mapper, CCVHardware: video Projector, camera, IR light, custom thermoformed structure
- (cap) Using Mad Mapper it was possible to tighten the projection beam onto the panel anchored in the center of the room, so as to create a floating element and at the
- (genuine) It is this kind of mapping that Leonard undertakes both in her work and through the form of the exhibition.” This description of Leonard as a mapper, a surveyor

### psi  [general] 총 22 / genuine 1 (4%)
- 분포: allcaps 9, cap 12, genuine 1
- (cap) As with Psi Girls , the effect is not so much that of a macabre horror films as of a participatory report that frames elusive phenomena in various narrative for
- (cap) Photo: Maria da Schio Susan Hiller, Psi Girls , 1999 (especially rearranged for the ex-church of San Francesco).
- (genuine) Now it’s operated at 1,000 psi and even 2,000.

### narcissus  [general] 총 124 / genuine 6 (5%)
- 분포: trunc 2, capinit 9, cap 105, urlish 2, genuine 6
- (cap) In the 1980s he discovered an allegory for his particular sensitivity in the myth of Narcissus, which he encountered in André Gide’s essay “The Treatise of Narc
- (cap) In the 1980s he discovered an allegory for his particular sensitivity in the myth of Narcissus, which he encountered in André Gide’s essay “The Treatise of Narc
- (genuine) Arguably, machines change their image according to human preference, making people as enamored of their machine selves as the mythical narcissus who fell deeply
- (genuine) Examples include a sunflower paired with concentric circles, a narcissus crowned by a pinwheel of primary colors, and tree blossoms accompanied by checkerboards

### pew  [general] 총 83 / genuine 4 (5%)
- 분포: allcaps 1, capinit 2, cap 74, hyph 1, noneng 1, genuine 4
- (cap) There are two paths for the golden-age American cartoon star: to be withdrawn, like the lascivious skunk Pepé le Pew, or, worse, to be reimagined as bad art, as
- (cap) This project has been supported by The Pew Center for Arts & Heritage through the Philadelphia Exhibitions Initiative with additional support from the Marketing
- (genuine) The pew Charitable Trusts conducted a survey published in april 2007 that examines “Teens, privacy and online social networks”.
- (genuine) The main inding of the pew study was: privacy is relinquished and individuals move about in a community in which they may know some members personally but, for 

### zeppelin  [general] 총 42 / genuine 2 (5%)
- 분포: cap 36, noneng 4, genuine 2
- (cap) Had they been alive and in possession of a quantum of humility, the Who’s Keith Moon and Led Zeppelin’s John Bonham likely would have acknowledged similar debts
- (cap) Media partners: Agerpres, Zeppelin, Arhitext, Igloo, arhiforum.ro, feeder.ro, Șapte Seri, Radio France Internationale
- (genuine) Whale was a veteran, having enlisted straightaways in the Worcestershire Infantry Regiment after seeing firsthand the zeppelin attacks on London depicted in Hel
- (genuine) Take Drawing for Mother (2007), both a ballpoint drawing and a painting, where a zeppelin hovers above a slim tower that extends in increments; or Residuum (201

### snipes  [general] 총 21 / genuine 1 (5%)
- 분포: allcaps 1, capinit 5, cap 14, genuine 1
- (cap) Clark began his association with BAMcinématek on the series “Space Is the Place: Afrofuturism on Film” in 2015 and has since curated “Behind the Mask: Bamboozle
- (cap) IN A STORM-TOSSED MODERN WORLD, Wesley Snipes’s Twitter feed is an island of calm.
- (genuine) It snipes at the present.

### stiller  [general] 총 21 / genuine 1 (5%)
- 분포: capinit 2, cap 17, noneng 1, genuine 1
- (cap) Like the central character, Fred Stiller, how might we recognise the unreality of our reality?
- (cap) ROGER GREENBERG(Ben Stiller), like the hyperarticulate, acid-tongued narcissists who precede him in writer-director Noah Baumbach’s oeuvre—Bernard Berkman in Th
- (genuine) All photographs are “stills,” of course, but Struth’s are stiller than most.

### ting  [general] 총 103 / genuine 5 (5%)
- 분포: trunc 34, allcaps 2, capinit 2, cap 58, hyph 2, genuine 5
- (cap) The Ringling Museum of Art in Sarasota, Florida, announced that it has received a major gift from the Ting Tsung and Wei Fong Chao Foundation.
- (cap) In recognition of the gift, the museum will rename the venue the Ting Tsung and Wei Fong Chao Center for Asian Art.
- (genuine) She collects and uses images, objects and sounds to create new contexts, incorpora¬ting traces of memory, history, and personal allusions.
- (genuine) Nehme will be tasked with “set[ting] an artistic vision with an advisory committee to invite curators to organize the exhibitions and events at BAC.”Related Dan

### frisk  [general] 총 41 / genuine 2 (5%)
- 분포: cap 32, hyph 7, genuine 2
- (cap) Rikke Frisk (DK), born in 1970, is the founder and co-director of the community focused culture planning company, Indgreb, based in Copenhagen.
- (cap) Digital Musics & Sound Art Ludger Brümmer, Cedrik Fermont, Rikke Frisk, Daito Manabe, Christine McLeavey Payne, and Ars Electronica Team u19—create your world S
- (genuine) A rippling Edwardian folderol of mansard roofs, turreted corners, and double-height archways, it boasted amenities that make today’s high-end condos look like g
- (genuine) If any more clarification is needed, take out your phone now and Google ‘stop and frisk’.

### shin  [general] 총 179 / genuine 9 (5%)
- 분포: allcaps 3, capinit 11, cap 147, hyph 8, urlish 1, genuine 9
- (cap) In the process, Kawakita also developed the Shin Kenchiku Kogei Gakuin (School of New Architecture and Design), which opened in a suburb of Tokyo in 1932.
- (cap) The exhibition draws a trajectory from historical works by Lynda Benglis, Teresa Burga, Eva Hesse, Maria Lassnig and Lee Lozano, artists widely associated with 
- (genuine) The portable system is an easy learning aid for shin prosthetics training, which translates walking movements into auditory feedback.
- (genuine) We are offered a glimpse of their legs ( Rene’s Legs , 2025), the word “SKIN” tattooed on their right shin, “NINA SIMONE” on their left.

### atoll  [general] 총 20 / genuine 1 (5%)
- 분포: cap 18, urlish 1, genuine 1
- (cap) Shot at the Bikini Atoll in the Marshalls Islands, the images of post-nuclear ruins and submerged infrastructure are accompanied by an impressive soundtrack by 
- (cap) thermonuclear test at Bikini Atoll.
- (genuine) As one of the world’s most low-lying atoll archipelagos, the Maldives faces an existential threat because of the rising sea levels caused by the climate change.

### krypton  [general] 총 20 / genuine 1 (5%)
- 분포: allcaps 7, cap 10, hyph 1, urlish 1, genuine 1
- (cap) You created the whole Krypton fantasy to escape the reality of your life… a reality you couldn’t face!” Uttered by Supergirl in Superman , no.
- (cap) His planet, Krypton, perished long ago.
- (genuine) Each one of the so-called noble gases (in order of density: helium, neon, argon, krypton, and xenon) to varying degrees circulates freely in our atmosphere, but

### frank  [general] 총 1882 / genuine 98 (5%)
- 분포: trunc 5, allcaps 51, capinit 192, cap 1530, urlish 3, noneng 3, genuine 98
- (cap) “Blue moon, you saw me standing alone / Without a dream in my heart / Without a love of my own,” wrote Lorenz Hart in his lyrics for Blue Moon, a song that in t
- (cap) Translated from German by Mel Greenwald Imagery, tonal spaces, text blocks, interaction and programming: Zelko Wiener & Ursula Hentschläger Translations: Englis
- (genuine) And then, of course, Mildred’s sexuality and the details of her erotic life are so frank and surprising and vivid and not at all what you expect—since we presum
- (genuine) Later, the Emirati writer and commentator Mishaal al Gergawi offered a frank appraisal of how things work: “I can come here, walk around Solidere, buy some art,

### hydra  [general] 총 134 / genuine 7 (5%)
- 분포: allcaps 6, cap 113, hyph 4, urlish 4, genuine 7
- (cap) More information on the activities related to the exhibition is available at www.macba.cat, where you can also find the date of the premiere of the film Hydra D
- (cap) Most compelling was the hypnotic film Barney made from last year’s Hydra performance,Blood of Two.
- (genuine) But delaying this admission does not arrest this growing hydra; it only postpones strategic thinking about how to counter it.
- (genuine) Given the timescale, we continue to believe in widespread individually-conceived sabotage as a means of fighting the hydra that is the corporate, but must admit

### marquis  [general] 총 57 / genuine 3 (5%)
- 분포: cap 49, urlish 5, genuine 3
- (cap) As the signifier of hip modernism, Grove Press published Beckett, Burroughs, and Genet, as well as Henry Miller and the Marquis de Sade.
- (cap) With: Lucy & Dave Ching, Henry Codax, Bernadette Corporation, franckDavid, Ayako Kiyosawa, Jules Marquis, Otto Mennings, Paul Owens, Galeria Perdida, Mai-Thu Pe
- (genuine) Galerie Buchholz brings a vintage woven rug by Frances Stark, and Pilar Corrias shows a Philippe Parreno marquis that will soon be at Gladstone.
- (genuine) He has come to meet a mysterious client (based on Massimiliano Palombra, a 17th-century marquis who created the legendary Porta Alchemica in his Roman villa).

### roach  [general] 총 38 / genuine 2 (5%)
- 분포: capinit 3, cap 27, hyph 1, urlish 5, genuine 2
- (cap) On one of these ventures, he heard the jazz all-star record Quintet of the Year, with bebop pioneer Max Roach on drums, which set him on his path.
- (cap) Stephanie Roach, director of the FLAG Art Foundation, served as an institutional advisor.
- (genuine) I sense in the hieroglyph of the slow roach the writing of the Far East.
- (genuine) I was especially thrilled by the steam funnels and adverts on the subway for the roach trap brand, Roach Motel, which read ‘Roaches check in, but they don’t che

### coward  [general] 총 19 / genuine 1 (5%)
- 분포: capinit 1, cap 15, urlish 2, genuine 1
- (cap) The profusion of dialogue, as well as the characters’ tendency to speak in paradoxes and express themselves with witticisms, recall plays by Oscar Wilde and Noe
- (cap) Injection!” Playing the monstrous, dying Sissy Goforth, who lives in a villa on an island in the Mediterranean that she has essentially declared a nation-state,
- (genuine) I would be a coward if I didn’t just because of a visa.

### hutch  [general] 총 19 / genuine 1 (5%)
- 분포: cap 16, urlish 2, genuine 1
- (cap) Todd, who was himself operating under long-distance control, presumably by Jeffries, and tells Hutch (Tim Roth) on the phone to order French fries.
- (cap) “We’re a nation of killers,” says Chantal to Hutch in the van, by way of shrugging off the day’s work.
- (genuine) Anticipating a corporate-sponsored hutch with shades of the Armory Show and its humdrum ilk, we were tickled to discover that the Dynasty VIP Lounge was located

### marl  [general] 총 19 / genuine 1 (5%)
- 분포: trunc 11, cap 7, genuine 1
- (trunc) It was not a prosperous or productive landscape, being used primarily for sheep rearing, as well as offering grazing for cattle, sand and gravel extraction, and
- (trunc) “Cinema is a world that is founded on desire: the desire of producers and directors to make movies with this or that actress, the desire of spectators to watch 
- (genuine) Outside Marres, Kaffe Matthews composes an audio-visual installation inspired by sharks for the marl caves of Sint Pietersberg.

### rune  [general] 총 19 / genuine 1 (5%)
- 분포: capinit 4, cap 13, urlish 1, genuine 1
- (cap) Later that day, we walked to the Public Transport Museum—home to Swedish artist Bella Rune’s gorgeous mohair-and-silk sculptures, floating like giant jellyfish 
- (cap) The Absence of Eddy Table Rune Spaans Eddy Table, known from the comics of Dave Cooper, makes his screen debut in this animated short.
- (genuine) Joe Davis engineered a strand of DNA to code for the Germanic rune for life.

### bender  [general] 총 163 / genuine 9 (6%)
- 분포: capinit 8, cap 141, hyph 1, urlish 4, genuine 9
- (cap) We had meetings to organize it, and since I was going to cover the costs, we called it “Cindy Sherman & her Girlfriends Invite you to a Dance Party…” and listed
- (cap) Credits: In collaboration with James Monaghan, Ashley Seifert, Jennifer Bender, Jeff Nivala, Seth Shipman, Conor Camplisson, Emma Kowal, Tom Bork, Bill McCarthy
- (genuine) After the audio-video bender happened in between the end of 90s and the first two decades of the new millennium to many contemporary composers, mostly belonging
- (genuine) After the audio-video bender happened in between the end of 90s and the first two decades of the new millennium to many contemporary composers, mostly belonging

### pope  [general] 총 428 / genuine 24 (6%)
- 분포: allcaps 4, capinit 40, cap 356, hyph 1, urlish 3, genuine 24
- (cap) That event missed several points, whereas Joselit’s essay productively brings us to William Pope.L’s work, the relevance of which is convincing.
- (cap) However, the work of Pope.L’s that I cited,Eating the Wall Street Journal, 1991–2000, did not enter my text as a representation of black bodies, abject and self
- (genuine) From a different perspective, Degas’sAfter the Bathwas again in Sylvester’s thoughts when discussing the remarkable Study after Velázquez1950 (private collectio
- (genuine) The cover of the 1975 catalogue raisonné of his prints, for example, features drawings—one of Al Capone, the other of the pope—by a Zurich Hells Angel who was a

### zen  [general] 총 357 / genuine 20 (6%)
- 분포: trunc 14, allcaps 8, capinit 6, cap 301, hyph 5, urlish 1, noneng 2, genuine 20
- (cap) Throughout his oeuvre, Byars combined motifs and symbols from Eastern traditions and civilizations, such as elements of Nô theater and Zen Buddhism, with a deep
- (cap) My conversation with John Armleder took place in between these two Zen-like aphorisms, repeated like inverted commas at the beginning and end of our chat.
- (genuine) I felt part of something great and zen and vast.
- (genuine) Field recording, electroacoustic, evanescent resonances, minimal acts full of organic substances, atmospheres finely wrought in the void by impenetrable geometr

### commonwealth  [general] 총 161 / genuine 9 (6%)
- 분포: allcaps 2, capinit 3, cap 145, urlish 2, genuine 9
- (cap) At some point, roughly 1971, Lucy took myself, Jackie Winsor, Charles Simonds and one other artist to Virginia Commonwealth University, where we spent a few day
- (cap) Virginia Commonwealth University in Richmond announced today that Joseph H.
- (genuine) Instead of peddling hope and visions of mutually shared commonwealth, authority is maintained by the production of synthetic fear and the need to secure propert
- (genuine) "Now it has become like the Sturla period in Iceland again," he said one day, referring to a famous saga of the thirteenth century, when warriors dismantled the

### breasted  [general] 총 18 / genuine 1 (6%)
- 분포: trunc 1, cap 1, hyph 15, genuine 1
- (hyph) In the magazine photo, its full page supporting the entire collage, a strange oval-framed portrait of a bare-breasted but elaborately necklaced woman hangs abov
- (hyph) Misshapen figures, seen with wide open mouths and gelatinous appendages, often multi-breasted and donned in malformed headdresses, wander through her canvases i
- (genuine) The figures are, in part, self-portraits: both have Smith’s face and flowing hair, but their furry, breasted torsos have goat forelegs, and their bottom halves 

### citron  [general] 총 18 / genuine 1 (6%)
- 분포: capinit 1, cap 15, hyph 1, genuine 1
- (cap) Whitney, John, Citron: (1968).
- (cap) “Photographic imagery in South Asia has become an effective means for the underrepresented to claim voice and political presence,” said Beth Citron, a curator a
- (genuine) Corners become crossroads where saliva mingles with crystals tasting of unripe citron, drying the dampness of your lips.

### giro  [general] 총 18 / genuine 1 (6%)
- 분포: allcaps 2, cap 15, genuine 1
- (cap) The Bonnefantenmuseum is a beneficiary of the Bank Giro Loterij.
- (cap) The Painted Bird: Dreams and Nightmares of Europeis made possible by Fonds 21, the Bank Giro Lottery Fund and more than 150 private donors that contributed to a
- (genuine) tris-tras, giro, fallo (2021), Patio de Luces (2022), and the operetta Arrela’t, nena, arrela’t (2019)—Pagès Rabal has instinctually followed the historical lay

### magi  [general] 총 18 / genuine 1 (6%)
- 분포: allcaps 7, capinit 1, cap 9, genuine 1
- (cap) The Making of a Triptych:The Annunciation and Adoration of the Magi1861 by Edward Burne-Jones
- (cap) RICHARD TAYLOR: creative director at Magi West Coast, LA He used to work for Information International, the company which later became Digital Productions.
- (genuine) Pilgrimage proves less pointless in Birdsong, Serra’s second feature (or third, if one counts the lost, and disavowed, 2003 film Crespiàas his first), as his th

### sultan  [general] 총 175 / genuine 10 (6%)
- 분포: capinit 23, cap 140, urlish 2, genuine 10
- (cap) Wiley; sculptors Richard Serra and Mark di Suvero; sound artist Bill Fontana; industrial designer Sara Little Turnbull; architect Lawrence Halprin; and photogra
- (cap) Sebald and an abhorrence of nonsocialized health care, Parrish director Terrie Sultan announced that Close, along with director-choreographer Patricia Birch, ch
- (genuine) This principle would become a justification for a system at the top of which we find the sultan and a hierarchy that functions with some semblance of a system o
- (genuine) Rolf Langenbartels About Sounding Bodies and Talking Clothes The great author Denis Diderot, one of the founders of the Encyclopédie Française has the jewels of

### shiner  [general] 총 53 / genuine 3 (6%)
- 분포: capinit 10, cap 39, hyph 1, genuine 3
- (cap) Kamps’s appointment comes on the heels of the gallery’s decision to hire Eric Shiner, the former senior vice president of contemporary art at Sotheby’s, as its 
- (cap) With Andy Warhol Museum director Eric Shiner doing the inviting, the Focus section—generally small, independent shops showing emerging or under-the-radar artist
- (genuine) In Ragged Dick he plays an early 20th century shoe shiner trying to earn enough cash for a ticket to the movies, an effort which eventually leads to his death.
- (genuine) In the Finnish director’s second film set in France after La Vie de Bohème(1992), former artist Marcel (André Wilms), now working as a shoe shiner in the port t

### die  [general] 총 14380 / genuine 827 (6%)
- 분포: trunc 65, allcaps 69, capinit 1965, cap 1105, hyph 60, urlish 359, noneng 9930, genuine 827
- (noneng) Die Wurzeln der Stadt Linz gehen zurück bis in die Zeit der Römer und Kelten, an die auch der Name des Kunst­ museums "Lentos" erinnert.
- (noneng) Die Wurzeln der Stadt Linz gehen zurück bis in die Zeit der Römer und Kelten, an die auch der Name des Kunst­ museums "Lentos" erinnert.
- (genuine) A Journal of Ideas, spring 2014 9 Obama’s speech highlights rise of 3D-printing, http:// www.cnn.com/2013/02/13/tech/innovation/obama-3dprinting/ 10 Marc Kowals
- (genuine) "It baffles me that this rhetoric of 'transcendenee via the Net' did not die a quick death a deeade ago.

### linden  [general] 총 139 / genuine 8 (6%)
- 분포: allcaps 1, capinit 5, cap 121, hyph 1, noneng 3, genuine 8
- (cap) Frequently, individual clothing textures get lost during the process of transfer and communication between the various data banks at Linden Labs.
- (cap) Residency at the European Space Agency (ESA) The recipient of the final network’s residency and yet at the same time the first art&science@ESA residency is Aoif
- (genuine) It will be fascinating to see how the artist-wanderer approaches this task; how, for example, Kentridge will animate the linden tree, with its words of love car
- (genuine) You will visit Faust’s study and witness Walpurgis Night as well as the dance under the linden tree.

### tropic  [general] 총 51 / genuine 3 (6%)
- 분포: trunc 23, allcaps 2, capinit 3, cap 19, urlish 1, genuine 3
- (trunc) The solution was to make a number of copies, both of Parangolé CapesandPenetrables, including the ‘environment’Tropicália.
- (trunc) One that he invented –Tropicália– became an elastic keyword for a group of musicians he knew, Caetano Veloso and Torquato Neto among them.
- (genuine) Recombining, for example, Broadway motifs with John Carpenter-esque jingles, angelic kids-chorales with Beyoncé riffs, and Catholic rite with Cal Artian legend,
- (genuine) Taken in the outer islands of Hong Kong, these tropic compositions of landscape art are restaged, observing smog and mountains in a setting atypical to where on

### minima  [general] 총 17 / genuine 1 (6%)
- 분포: capinit 1, cap 14, noneng 1, genuine 1
- (cap) Like the subject of that quote from that sinister book published in 1951, titled Minima Moralia , in Majerus’s aesthetics we encounter “the hysteric, who desire
- (cap) Adorno, Minima Moralia: Reflexionen aus dem Beschädigten Leben (Frankfurt am Main: Suhrkamp, 1951), 163.
- (genuine) All such models have yet to be embedded into a more minima l (reversible) universe.

### psycho  [general] 총 283 / genuine 17 (6%)
- 분포: trunc 11, allcaps 2, capinit 5, cap 69, hyph 179, genuine 17
- (hyph) nourishes himself on pizza, hamburgers, Coca-Cola, beer, potato crisps and appetite reducing and performance boosting psycho-pharmaceutical products.
- (hyph) HAVIDOL™ is an artful parody of a new kind of gold rush, heralding an era in which pharmaceutical companies mine psycho-chemicals for a public that is ready to 
- (genuine) In the big picture, things are getting more abject by the minute now that we have a psycho neofascist in the White House.
- (genuine) A quick look to the title track video is enough to realise how much these imaginary worlds are both contaminated and contradictory: dark circus music passages w

### bong  [general] 총 50 / genuine 3 (6%)
- 분포: trunc 2, allcaps 2, capinit 8, cap 32, hyph 3, genuine 3
- (cap) Installation view Installation view Untitled, 2010 Withdrawal 2, 2010 The Wrong Craving, 2010 Untitled, 2010 Tinea, 2010 Untitled, 2010 Sold My Tusks, 2010 Ever
- (cap) Installation view Installation view Untitled, 2010 Withdrawal 2, 2010 The Wrong Craving, 2010 Untitled, 2010 Tinea, 2010 Untitled, 2010 Sold My Tusks, 2010 Ever
- (genuine) He reprised this role for the Artforumad on the occasion of his 2013 exhibition “1 O O O I S L A N D”: He sits on a plush couch, smoking a bong jury-rigged from
- (genuine) For viewers of my generation, watching the film today brings back memories of Nirvana, Doc Martens, and the scent of stale bong smoke.

### badlands  [general] 총 66 / genuine 4 (6%)
- 분포: allcaps 1, capinit 14, cap 47, genuine 4
- (cap) He’s also known for his performances of Beckett’s Waiting for Godot_ in New Orleans after Hurricane Katrina, and more recently for starting a publishing imprint
- (cap) No one at the Badlands office can.
- (genuine) The decision to revisit recent histories of cultural production in Beirut, which remain far from settled in the narrative badlands of Lebanon’s long civil war, 
- (genuine) Consisting of five brightly painted boulders stacked in the form of a contemporary cairn,Miami Mountain(2016) finds its geological inspiration from "hoodoos," r

### monsieur  [general] 총 49 / genuine 3 (6%)
- 분포: capinit 4, cap 42, genuine 3
- (cap) Arnault reminded us that Monsieur Dior was a gallery owner before he became a designer; so art was in the brand’s DNA, as they say in the industry.
- (cap) The artist often jokes in letters about thecanon bibital(private “gun”), and around this time addressed a postcard to “Monsieur ELT Mesens (manufacturer of mars
- (genuine) For untitled 1995 (bon voyage monsieur ackermann) , Tiravanija and German artist Franz Ackermann drove a converted yellow Opel Commodore from Berlin to Lyon, wh
- (genuine) Everybody pretended to think she was a man dressed up and kept saying ‘ah monsieur, monsieur’.

### shim  [general] 총 33 / genuine 2 (6%)
- 분포: capinit 1, cap 24, urlish 6, genuine 2
- (cap) Press contact:Shim Bokeum, Public Relations TeamT +82 2 2014 6553 /bokeum.shim@samsung.com
- (cap) Howard Sutcliffeof Shim-Sutcliffe Architects.
- (genuine) Technically they continue the collage methodology I’ve always exhibited but these forefront more recent pigment transfer techniques with transparent to opaque l
- (genuine) Like a giant old-growth shim, you continue to level this drawn world.

### senate  [general] 총 178 / genuine 11 (6%)
- 분포: capinit 4, cap 159, hyph 1, urlish 3, genuine 11
- (cap) On December 10, the Senate passed a bill that will shield works loaned to the US from foreign arts institutions from being confiscated, report Sophia Kishkovsky
- (cap) The center, which will include a library containing Obama’s presidential archives and a museum dedicated to his presidency, will be built in Chicago’s South Sid
- (genuine) The US senate passes a $1.9 trillion relief bill.
- (genuine) The quadrennial award, which includes an endowment of nearly $12,500, was founded in 1929 by the German senate on the bicentennial of philosopher Gotthold Ephra

### champs  [general] 총 48 / genuine 3 (6%)
- 분포: cap 41, hyph 1, noneng 3, genuine 3
- (cap) With this iconic work of modernity, premiered in 1913 at the Théâtre des Champs-Élysées in Paris, Stravinsky himself had broken new ground, and in the following
- (cap) Le Mondereports that the Bibliothèque Publique d’Information will be housed in the Lumière building, near Paris’s Bercy Village, while the Pompidou will mount e
- (genuine) Interleaved with images of female tennis champs, this tidy, portable volume will become the dog-eared best friend to anyone who cares about the embattled art of
- (genuine) I’m doing two-part exhibition— Pendant que les champs brûlent —from the end of May until the end of July.

### ere  [general] 총 48 / genuine 3 (6%)
- 분포: trunc 39, capinit 2, cap 1, hyph 1, urlish 1, noneng 1, genuine 3
- (trunc) Größere Kugeln bedeuten größere Effektstärke (geringere p-Werte).
- (trunc) Größere Kugeln bedeuten größere Effektstärke (geringere p-Werte).
- (genuine) The encomium to the Miletus torso, tinctured by this recent rejection, ends with the oft-quoted lines, “[H]ere there is no place / that does not see you.
- (genuine) It was the second film with Marilyn that I was watching and the extract which fascinated me most was the only part in which Marilyn disappears to give place to 

### dimes  [general] 총 32 / genuine 2 (6%)
- 분포: capinit 4, cap 26, genuine 2
- (cap) – Sam, comment on “My Own Dimes Square Fascist Humiliation Ritual” by Mike Crumplar
- (cap) In his Baffleressay “Escape from Dimes Square,”Will Harrison notesthat “‘Dimes Square’ signifies a bit more than it used to, looming larger in the city’s imagin
- (genuine) We had a lot in common, she and I, finding roundabout ways of dissolving into ourselves, saving dimes, engaging in desultory efforts to test the limits of our o
- (genuine) But one has to assume that Capps no longer worries about the nickels and dimes of these particular gigs.

### draper  [general] 총 32 / genuine 2 (6%)
- 분포: allcaps 1, capinit 3, cap 26, genuine 2
- (cap) Faced with the inevitable (and market-driven) descent into cliché that Rubin described—a descent fueled by an art world newly filled with eager collectors of co
- (cap) The intense romanticizing of that era today comes from popular culture, through television shows such as Mad Men, which is set in 1958, where everything in Don 
- (genuine) Thuring has continued this exploration by stretching as her canvas, a registered Neapolitan tartan produced by local draper ISAIA, a fabric producer established
- (genuine) The first, that of draper, businessman, Auckland city councillor and philanthropist, John Court (1846–1933), is synthesised with the recognisable narrative of t

### bate  [general] 총 16 / genuine 1 (6%)
- 분포: capinit 3, cap 10, hyph 2, genuine 1
- (cap) S ee Walter Jackson Bate “Negative Capability”, in John Keats , (Belknap Press:Cambridge, 1963), p.
- (cap) See Walter Jackson Bate “Negative Capability”, in John Keats , (Belknap Press:Cambridge, 1963), p.
- (genuine) The show is curated by Margot Norton and Jamillah James with Jeanette Bisschops and Bernardo Mosqueira and titled “Soft Water Hard Stone” (openuntil January 23,

### mezzo  [general] 총 16 / genuine 1 (6%)
- 분포: cap 4, hyph 4, noneng 7, genuine 1
- (noneng) Nelle Istanbul Improv Session del 4 Maggio Alban Lotz è accompagnato da Sevket Akinci alla chitarra, da Korhan Erel che manipola suoni dal laptop per mezzo di p
- (noneng) Terre di mezzo, ISBN 8889385375
- (genuine) For pleasure Cornell once read out to his invalid brother an account of Maria’s first performance in New York.9A third figure in Cornell’s operatic pantheon was

### nope  [general] 총 16 / genuine 1 (6%)
- 분포: allcaps 7, capinit 3, cap 5, genuine 1
- (allcaps) With STWST48x10 NOPE, Stadtwerkstatt is ­holding the 10th edition of its annual 48-hour non-stop showcase extravaganza STWST48 in September 2024: With NOPE, STW
- (allcaps) With STWST48x10 NOPE, Stadtwerkstatt is ­holding the 10th edition of its annual 48-hour non-stop showcase extravaganza STWST48 in September 2024: With NOPE, STW
- (genuine) When it occasionally spat me up, my snippets of awareness gave me the sense very much of fast-forwarding through a video file, finding that, nope, not much was 

### steeds  [general] 총 47 / genuine 3 (6%)
- 분포: capinit 1, cap 23, urlish 1, noneng 19, genuine 3
- (cap) Goshka Macuga, Picture Room , 2003 by Lucy Steeds from THE ARTIST AS CURATOR #7 – in Mousse #48 .
- (cap) THE ARTIS T AS CURATOR #7 – in Mousse #48 Andy Warhol, Raid the Icebox I, with Andy Warhol , 1969 – ANTHONY HUBERMAN Goshka Macuga, Picture Room , 2003 – Lucy S
- (genuine) Between prep for this latest relapse back into fashion naraka (“reinforcing the spectacle by denouncing it in the abstract”), the closest I get to cowboys is TF
- (genuine) They seem to fly across a black void, conforming to the Iliadic formula of “swift-footed steeds,” but also seeming to refer to nothing except themselves.

### fry  [general] 총 186 / genuine 12 (6%)
- 분포: allcaps 3, capinit 9, cap 153, hyph 6, urlish 3, genuine 12
- (cap) With Ben Fry, Reas initiated Processing in 2001; Processing is an open-source programming language and environment for the visual arts.
- (cap) With a comprehensive and diverse program, push.conference lives up to this with speakers from design consultancies,, companies like Google Ventures on to brilli
- (genuine) She’ll fry them in Crisco, in the electric skillet.
- (genuine) Angelou began her career in roles including a fry cook and nightclub dancer, jobs that eventually led her to become a journalist and editor in Egypt and Ghana d

### babel  [general] 총 136 / genuine 9 (7%)
- 분포: capinit 1, cap 125, urlish 1, genuine 9
- (cap) Also on the ground floor, five backlit collages look back on Hiwa K’s early school days ( Ball ballat Babel , 2023).
- (cap) In the monumental sculpture made up of stacked suitcases, »Babel II« (1998), which is one of the main oeuvres of the artist, a babble of voices in diverse langu
- (genuine) Good insights from the history of radio and newspapers reinforces the current information environments (“from the highly passive tv to the personal productive n
- (genuine) Good insights from the history of radio and newspapers reinforces the current information environments (“from the highly passive tv to the personal productive n

### ruff  [general] 총 89 / genuine 6 (7%)
- 분포: capinit 7, cap 74, urlish 2, genuine 6
- (cap) With this in mind, Pryde’s exhibition—her guinea pigs in particular—must be regarded as a site-specific intervention transgressing the likes of Andreas Gursky, 
- (cap) Robinson, Rossella Biscotti, Signe Marie Andersen, Sophie Calle, Thomas Ruff, Thomas Struth, Torfinn Michaelsen, Tom Sandberg, Torbjørn Rødland, Vibeke Tandberg
- (genuine) The horse begins to rock again, a ray of light through the creaking door reveals the face of a red-and-white Pierrot lying with its ruff against the wall atop a
- (genuine) In the drypoint etching Pierrot, Portrait of the Lady A.C., 1888, the subject wears the conical hat and ruff of the pierrot costume and her expression is one of

### nuke  [general] 총 15 / genuine 1 (7%)
- 분포: allcaps 1, cap 13, genuine 1
- (cap) Software: Maya (Arnold), After Effects, Nuke, Photoshop.
- (cap) Since November 2012 ­Christian has been a freelance Nuke compositor and coder living in Berlin.
- (genuine) He’s like, “Fuck all this shit, let’s nuke the planet from outer space, get the fuck out of here, and deal with the legal ramifications later!” SONDRA Laters!

### rives  [general] 총 15 / genuine 1 (7%)
- 분포: trunc 11, cap 3, genuine 1
- (trunc) Precise and objective, his works can be seen as post-modern dérives; close readings which position a viewer, a reader, in new emotive proximities with the “stuf
- (trunc) The Situationist International translated the fragmentary experience of the labyrinth into their urban dérives and theoretical texts, most prominently in Asger 
- (genuine) Metaxu (les rives où vivent mes songes) showcases the Swiss mountains and landscapes of the Neuchâtel region through her evanescent, dreamlike paintings.

### shoplifter  [general] 총 15 / genuine 1 (7%)
- 분포: capinit 4, cap 10, genuine 1
- (cap) The year 2019 at Kiasma will kick off in February with a show by the internationally renowned New York-based Icelandic artist Hrafnhildur Arnardóttir, also know
- (cap) Joy, playfulness, and innocence are potential experiences Shoplifter conveys within her art.
- (genuine) Courtesy: Cecilia Pavón and Galería Nora Fisch, Buenos Aires The stench of a potential ammonia shoplifter spawned an embarrassment of neighborly espionages, whi

### den  [general] 총 4041 / genuine 279 (7%)
- 분포: trunc 49, allcaps 7, capinit 25, cap 204, hyph 3, urlish 26, noneng 3448, genuine 279
- (noneng) Im Zweiten Weltkrieg, vor über 60 Jahren, machten die Nationalsozialisten durch den Aufbau der Rüstungsindustrie aus Linz das Zentrum der Schwerindustrie in Öst
- (noneng) In den 1 970er Jahren entsteht eine Vielzahl von Intitiati­ ven.
- (genuine) In the immersive exhibition Model Collapse, Cyanne van den Houten and Ymer Marinus depict the landscape from which generative AI emerges.
- (genuine) Software Man and Milestones Benjamin Heidersberger / Bernd van den Brincken It has rarely been the case in the entire history of mankind that a tool managed to 

### hangar  [general] 총 375 / genuine 26 (7%)
- 분포: trunc 1, allcaps 5, capinit 14, cap 317, hyph 7, urlish 5, genuine 26
- (cap) He has held residencies at Hangar, HISK, and Sarai New Delhi.
- (cap) Smith, Maurice Tuchman, Juan Fassio, and the Margo Leavin Gallery, and has published numerous papers and catalogue essays for the Istanbul Biennale, the Fondazi
- (genuine) Once in town, my target was the Parrish Art Museum’s Midsummer Party, the institution’s last annual fundraiser before it ups sticks to a brand new Herzog & de M
- (genuine) Work in the hangar is filmed in a hypnotic form of visual anthropology that is at once seductive, because flowers can be beautiful, and terrifying, because the 

### spiel  [general] 총 101 / genuine 7 (7%)
- 분포: trunc 4, capinit 3, cap 83, hyph 1, urlish 2, noneng 1, genuine 7
- (cap) University of Illinois at Urbana, Champaign Intel Labs Peter van Haaften (CA), Michael Montanaro (CA) Spiel | an in-situ performance for prepared mouth While ab
- (cap) “Please knock!” Szerafina Roxaná Thalia Schiesser (DE) Klopfmaschinen An interactive sound installation for communicating through walls © Spiel und Objekt
- (genuine) John Waters appeared too, but only via prerecorded video (his typically droll spiel was a good five times the length of honoree Ursula Hauser’s nervy acceptance
- (genuine) Home Sweet Home: Love Pool 8(2022) plays out a similar spiel, albeit in a swimming pool shallower in terms of decor and taste.

### lambda  [general] 총 57 / genuine 4 (7%)
- 분포: trunc 3, capinit 3, cap 47, genuine 4
- (cap) 40 x 40 cm, Lambda print on matte photographic paper mounted on Dibond backing, 200,— Eur (+ shipping).
- (cap) at Lambda LambdaLambda², Prishtina until January 28, 2023
- (genuine) Five lambda prints on an aluminium base, mounted under acrylic.
- (genuine) “In physics, the lambda is the sign for a frequency, which we liked.

### baker  [general] 총 395 / genuine 28 (7%)
- 분포: trunc 2, allcaps 4, capinit 32, cap 327, urlish 2, genuine 28
- (cap) Founded by art consultant Lisa Fehily, Finkelstein Gallery will represent a roster of ten artists: Cigdem Aydemir, Kate Baker, Monika Behrens, Coady, Deborah Ke
- (cap) He later exhibited at Susan Caldwell, Andre Zarre, and Elaine Baker galleries, and was given survey shows at Bennington College and Hunter College.
- (genuine) Instead I flew to New York and became a doughnut baker in Connecticut.
- (genuine) I was also working there, trying to teach art – combined with a job as a pizza baker in the student café – but I don’t really remember how serious we were about

### lux  [general] 총 140 / genuine 10 (7%)
- 분포: allcaps 60, capinit 8, cap 59, hyph 2, urlish 1, genuine 10
- (allcaps) SUUM X is pleased to present LUX: Poetic Resolution, a major new exhibition of contemporary new media art.
- (allcaps) Following the successful large-scale media installation exhibition LUX: New Wave of Contemporary Artin London (2021), the second edition LUX: Poetic Resolutioni
- (genuine) Test scenes for Karsten Schmidt‘s new lux4j (Luxrender) exporter library for Processing/Java.
- (genuine) Heraclitus’ philosophy, with its understanding of reality as constant state of lux, now stands not only for innovative management training methods, but also for

### sojourner  [general] 총 28 / genuine 2 (7%)
- 분포: capinit 3, cap 23, genuine 2
- (cap) We will also feature an exhibition on Sojourner2020, the first international art open call that took a trip to the International Space Station this March.
- (cap) For eighteen years, Mulherin ran her eponymous gallery out of multiple storefronts in Toronto, showcasing emerging Canadian artists including Dean Baldwin, Sojo
- (genuine) Spanning reappropriated amateur footage across the 20th century, the sojourner’s gaze—distanced, distorted and even voyeuristic—shows tropes and patterns.
- (genuine) The Sourcebooklearns from Nishikawa Kimitsu, a Yokohama day labourer who embodies what it means to be a curious sojourner, an autodidact adrift in the universe.

### alp  [general] 총 14 / genuine 1 (7%)
- 분포: trunc 1, allcaps 3, cap 8, hyph 1, genuine 1
- (cap) Screening with Ambling Alp Radical Friend, USA, 2009, 4 minutes
- (cap) The fire pit is part of a series of works that Gindre began in 2005 on the Älggi Alp, which is the measured geological center of Switzerland.
- (genuine) Her face is hidden by a large, rectangular mask comprised of huge cubist eyes, a nose like an alp and a ferocious mouth, topped with a crown as jagged as a saw.

### celled  [general] 총 14 / genuine 1 (7%)
- 분포: hyph 13, genuine 1
- (hyph) Computerless industrial machinery exhibits the behavioral flexibility of single-celled organisms.
- (hyph) The purely chemical responses of single-celled creatures led to tropistic behavior.
- (genuine) The apartment she lived in wasn’t owned by the bank that figured in her work as a celled monolith bound in bungee cords.

### coliseum  [general] 총 14 / genuine 1 (7%)
- 분포: cap 13, genuine 1
- (cap) It combines stop motion and live action filmmaking shot at the Harvard University Coliseum in Boston (1935) and the Municipal Stadium in Florence (1932), built 
- (cap) It combines stop motion and live action filmmaking shot at the Harvard University Coliseum.
- (genuine) In the stunning 2006Tension Building—an unfortunate omission from the Anthology program, though it can be found in its entirety on herwebsite—she uses stop-moti

### guarani  [general] 총 14 / genuine 1 (7%)
- 분포: cap 12, urlish 1, genuine 1
- (cap) She is of Guarani Nhandewa heritage and is currently a doctoral candidate in social anthropology at the Universidade Federal do Rio de Janeiro.
- (cap) When we speak about histories, we speak about ancestral knowledge, and the objective here is to tell these histories from an indigenous perspective about ‘ywy r
- (genuine) In The Passage, her new installation at Eye, she works with heat images and voices from northern Argentina (qom, quechua, aymara, wichi and guarani), yet anothe

### meson  [general] 총 14 / genuine 1 (7%)
- 분포: capinit 4, cap 7, urlish 2, genuine 1
- (cap) He recently edited the anthology Alleys of Your Mind: Augmented Intelligence and Its Traumas (Meson Press) among other books.
- (cap) He recently edited the anthology Alleys of Your Mind: Augmented Intelligence and Its Traumas (Meson Press) among other books.
- (genuine) The theme is the title of a new book Accidental Archivism: Shaping Cinema’s Futures with Remnants of the Pastedited by Vinzenz Hediger and Stefanie Schulte Stra

### necked  [general] 총 14 / genuine 1 (7%)
- 분포: trunc 1, cap 1, hyph 11, genuine 1
- (hyph) At the by-the-pound thrift store a pullover spoke to me, V-necked and a pointy color, very ’70s, a sort of static design of stripes across it.Yes.
- (hyph) Filmed on Düsseldorf’s Königsallee employing state-of-the-art technology, the work documents the daily flight of ring-necked parakeets along the shopping strip 
- (genuine) As the auction drew to a close, I swapped cards with a staffer from Third Eye PR, necked an espresso, pocketed some chocolates, and that was my night.

### ordinate  [general] 총 14 / genuine 1 (7%)
- 분포: allcaps 4, hyph 9, genuine 1
- (hyph) So if you assign the texture co-ordinate 0.5, 0.5 to a vertex, the middle of the image will appear at that point.
- (hyph) When creating the vertices using the append Vertex() and append ColorRGB() methods, use the append TexCoord() method to create a texture co-ordinate.
- (genuine) by Pierre Bal-Blanc At public conferences, I usually introduce my curatorial practice by referring to two simple examples that illustrate the two axes—the absci

### parfait  [general] 총 14 / genuine 1 (7%)
- 분포: cap 9, urlish 3, noneng 1, genuine 1
- (cap) With Pascale Obolo,Parfait Tabapsi,Yaiza Camps,Moritz GrünkeandMichalis Pichler.
- (cap) Editors: Yaiza Camps, Moritz Grünke, Pascale Obolo, Michalis Pichler, Parfait Tabapsi.
- (genuine) And of the sea buckthorn berry parfait we were served for dessert that night as part of Arja Lehtimäki’sFoodscape?

### pinker  [general] 총 14 / genuine 1 (7%)
- 분포: capinit 1, cap 12, genuine 1
- (cap) http://www.ey.com/AT/de/Newsroom/ News-releases/PM_2013_EY-Studie--US-Unternehmen-h%C3%A4ngen-europ%C3%A4ische-Konkurrenz-ab 18 Steven Pinker, “Personal Genomic
- (cap) One of the leading lights of this positive future outlook is Harvard Professor Steven Pinker, a linguist, journalist, experimental psychologist, and cognitive s
- (genuine) To compensate for the lack of the mid-tone provided by the priming, and to keep the colouring of Keable’s face consistent with his companions’, Gainsborough use

### sleeved  [general] 총 14 / genuine 1 (7%)
- 분포: hyph 13, genuine 1
- (hyph) During the summer, this perambulatory team of female-inclined people wore a light, cap-sleeved garment called the ABW Pattern #3 Dress in a variety of shades.
- (hyph) During the autumn months, when I visited, they wore the long-sleeved, somberly black ABW Pattern #2 Dress, what the artist calls a “dress designed for strolling
- (genuine) Nine glass sheets are placed on curved steel, sleeved by rubber.

### commodore  [general] 총 82 / genuine 6 (7%)
- 분포: capinit 1, cap 75, genuine 6
- (cap) In 1981, five years after Commodore had also entered the market, what was then the sixth largest company in the world, also put a small, dainty PC on the market
- (cap) Two years later, Apple, Commodore and Radio Shack had small personal computers on the market which still couldn't do very much, but which sold fantastically wel
- (genuine) “Low Level All Stars” showcases the best cracker tags selected from over 1,000 games available for the commodore 64 computer.
- (genuine) All cracker tags have been re-cracked by beige and RSG and extracted as stand-alone commodore animations.

### kilter  [general] 총 55 / genuine 4 (7%)
- 분포: hyph 48, urlish 3, genuine 4
- (hyph) Unlike those surprisingly playful, embarrassing, or silly moments that humanize now-iconic artistic figures while they were cavorting in the South of France and
- (hyph) Accompanied by website screenshots, architectural renderings, and Photoshop collages, the two-thousand-word text looked back on the preceding decade through an 
- (genuine) Her associations with spiritualism and her rich and varied vocabulary of abstract and symbolic forms had been deemed out of kilter with the formal austerity of 
- (genuine) Such moralistic readings seem out of kilter with the playful feel and disconnected narrative structure of the series.

### tramway  [general] 총 55 / genuine 4 (7%)
- 분포: allcaps 1, capinit 4, cap 44, urlish 2, genuine 4
- (cap) In careful continuity with the language of previous works, Rooney’s installation at Tramway draws on a familiar set of textures and reference points to create a
- (cap) This exhibition has been co-commissioned by Tramway and MAP, in association with the MAP commission Others got wings for Flying.
- (genuine) Too, it lent itself well to reproduction, appearing on the pencil cases referenced by Macron, as well as school bags, notebooks, and the steps of the tramway in
- (genuine) Here are a few examples: • Japan’s zero-emission Aero-Train: a metropolitan tramway hovering ten centimeters above the ground that can carry 335 passengers at a

### mister  [general] 총 41 / genuine 3 (7%)
- 분포: capinit 1, cap 36, urlish 1, genuine 3
- (cap) She discussed her new album Mister Heartbreak, her influence from Word Jazz radio storyteller and fellow Chicagoan Ken Nordine, and her attraction to the comple
- (cap) As a freelance writer living in Amsterdam, Hellemans wrote several articles for online art magazine Mister Motley, which connects art to everyday life.
- (genuine) Love had included two objets: one a white bridal dress with “Not my cunt on my dime mister” embroidered on it in red; one vitrine displaying a “glass slipper” a
- (genuine) Keuner—mister nobody—points to Walter Benjamin’s plea to replace doxa with an impoverishment of theory that can meet the realities of impoverished experience.

### goggle  [general] 총 27 / genuine 2 (7%)
- 분포: capinit 1, cap 15, hyph 9, genuine 2
- (cap) The software, which uses the API Goggle adds random terms ('seeds', ie seeds) looking set, combining them into a path parallel to the intentional, the results a
- (cap) The perceptive revolution enabled by Goggle Earth is the one of being able to visually navigate most part of the world (including your own neighborhood) through
- (genuine) But the aversion to the "goggle box" is nothing more than the expression 01 the gen­ eral human need lor "outside" where one can make "experiences 01 one's own.
- (genuine) But the aversion to the "goggle box" is nothing more than the expression of the general human need for "outside" where one can make "experiences of one's own".

### ware  [general] 총 93 / genuine 7 (8%)
- 분포: trunc 17, allcaps 1, capinit 4, cap 44, hyph 10, urlish 8, noneng 2, genuine 7
- (cap) Ben Ware confronts the many real threats of the end and of extinction that define our shared present.
- (cap) Ben Ware—Nothing But the End to Come?
- (genuine) On one of the walls of the gallery are showcased the works influenced by the Korean “white porcelain ware,” especially the aesthetics embodied in moon jars, whi
- (genuine) The post-human movement’s pipe dream of soon being able to transform human beings into nomadic software entities takes an interesting turn in the emerging inter

### cola  [general] 총 170 / genuine 13 (8%)
- 분포: trunc 1, capinit 3, cap 149, urlish 4, genuine 13
- (cap) nourishes himself on pizza, hamburgers, Coca-Cola, beer, potato crisps and appetite reducing and performance boosting psycho-pharmaceutical products.
- (cap) Ramos often staged his subjects—nearly always nude women—with consumer products: behind Coca-Cola glasses, astride cigars, emerging from candy wrappers or banan
- (genuine) He printed politically critical messages onto coca cola bottles and banknotes, putting the objects back into circulation.
- (genuine) Inside the adjacent container, Duan Jianyu’s ink paintings on flattened cardboard boxes caught my eye, their corrugated lines and cola can rings still visible.

### tee  [general] 총 65 / genuine 5 (8%)
- 분포: trunc 1, allcaps 1, capinit 4, cap 46, hyph 2, urlish 6, genuine 5
- (cap) That moment, I noticed a familiar face—one that I immediately recognized as belonging to an iconic painting permanently displayed at the National Gallery Singap
- (cap) I had an idea to write about the weather while drinking tea at Tee-di-um, but that would have been too apparent.
- (genuine) Showing up unannounced on a motorcycle, clad in a punk-ass black leather jacket, a white-and-navy ringer tee, and an oversize army beret, Wally has transcended 
- (genuine) His eurrent projeets include a web interaetive seulptural fountain in Aspen, and a historical perspeetive on a few people who shared their tee nage years with E

### archer  [general] 총 39 / genuine 3 (8%)
- 분포: capinit 2, cap 33, hyph 1, genuine 3
- (cap) The Courtauld Institute doctoral dissertation of Petrine Archer-Straw, who had been a colleague at the NGJ in the mid–1980s, explored similar subject matter and
- (cap) One of Henry Moore’s outdoor sculptures,Die Archer, is on long-term loan from Berlin’s National Gallery in LWL’s central square.
- (genuine) The work’s own title is borrowed from recent graffiti the artist saw in London and harks back to the appearance on Downing Street on February 29, 1940, of a Rob
- (genuine) The targets are often in various states of decomposition (and pierced differently based on the experience of the archer).

### aye  [general] 총 26 / genuine 2 (8%)
- 분포: allcaps 2, capinit 1, cap 21, genuine 2
- (cap) The California Institute of the Arts announced that multidisciplinary artist Hock E Aye Vi Edgar Heap of Birds will be awarded an honorary doctorate of arts deg
- (cap) Scott Gallery is proud to present a solo exhibition by Hock E Aye Vi Edgar Heap of Birds.
- (genuine) Most recently, she curated A Field (2020), the first museum solo by Kandis Williams; Dineo Seshee Bopape’s solo show Ile aye, moya, là, ndokh… harmonic conversi
- (genuine) There, the whole world is formed of such, and far brighter and purer than they; part sea-purple of a wonderful beauty, a part like gold; a part whiter than alab

### aggrandizement  [general] 총 13 / genuine 1 (8%)
- 분포: hyph 12, genuine 1
- (hyph) The question is then how the global museum situates itself within this trajectory in an age of museum self-aggrandizement through expansions, speculations, and 
- (hyph) Although Beuys didn´t talk about the quality of creative behaviour, he behaved like a mythologized star, displaying behavior THWAITES assessed as “gross self-ag
- (genuine) If biography serves as a literary aggrandizement and idealization of its subject, portraiture’s value is situated in its inherent criticality—not only toward it

### brownie  [general] 총 13 / genuine 1 (8%)
- 분포: cap 12, genuine 1
- (cap) He received his first camera, the Kodak Brownie, in 1944 but studied painting at the University of Alabama where he graduated in 1958 and also received a master
- (cap) During his studies, he bought an old American Brownie camera at a second-hand market, and began to use photography and film to document the suppression of the p
- (genuine) Inside were two puny cuts of just one brownie; I must have felt cut down to size myself.

### linker  [general] 총 13 / genuine 1 (8%)
- 분포: allcaps 2, cap 8, noneng 2, genuine 1
- (cap) And my then-husband, Mark Segal, was studying film with Annette Michelson and working in the film/publicity department at Mo MA with Kate Linker, Roberta Smith 
- (cap) Referring to a number which represents, among many things, the difference, in years, between the life expectancy of a jamaican and a swedish person, Nine(9) is 
- (genuine) Technologies used:– Custom linker with custom gzip-compressor– import by hash for system libraries– “pure” shader (GLSL) visual– DLSSynth for audio– Mandelbox s

### madras  [general] 총 13 / genuine 1 (8%)
- 분포: cap 12, genuine 1
- (cap) Printed in Madras (now Chennai), India, and sold throughout the United States for a few dollars each, Hanuman’s books were the outcome of the two founders’ obse
- (cap) It is most clearly attributable to the Indo-Hungarian artist Amrita Sher-Gil, who trained in Paris in the 1930s, and it develops in the late 1940s in Bombay, as
- (genuine) Aitken, on the other hand, was attired in a bright madras plaid shirt with a label that said, HELLO, MY NAME IS DOUG stuck onto it.Related Mon oncle d’AmériqueB

### pita  [general] 총 13 / genuine 1 (8%)
- 분포: allcaps 1, cap 11, genuine 1
- (cap) Rehberg, aka Pita, iswell known either as an electronic music author and dj, collaborating with such musicians as Christian Fennesz and Jim O’Rourke.
- (cap) We won’t mention anyone in particular, because with names such as @c, Christoph de Babalon, Jorge Sánchez-Chiong, Cindytalk, Goner, Pita, Rashad Becker, Arturas
- (genuine) Somebody gave the birds pita bread, which they can’t fit in their bills, they can’t pick it up, they’re all hopping around So Ho flinging this bread around like

### prat  [general] 총 13 / genuine 1 (8%)
- 분포: cap 11, hyph 1, genuine 1
- (cap) Curators: Christian Alandete, Sebastiano Barassi, Jean-Louis Prat
- (cap) 10 Jean Prat, “La Regle du jeu,” in Analyse des films de Jean Renoir (Paris: Institut des Hautes Etudes Cinématographiques, 1966), 87–88, quoted in Charles Will
- (genuine) His repeated prat falls land somewhere between theatrical melodrama and possible suicide attempts.

### stargazer  [general] 총 13 / genuine 1 (8%)
- 분포: cap 8, hyph 4, genuine 1
- (cap) Mamma Andersson’s “Stargazer II”
- (cap) The on site and online visitors / participants of the Solar Orchard Garden are invited to participate in two complex experiences: Stargazer and Amazonia.
- (genuine) Erudite scholar, transcendent stargazer, angsty adolescent, obsessive fan, etc.

### talon  [general] 총 13 / genuine 1 (8%)
- 분포: trunc 1, cap 5, hyph 6, genuine 1
- (hyph) Hands are surrogates and metonyms, extremities that preserve in bronze the friction ridge on a fingertip; an odd, talon-like nail; or plump pockets of skin else
- (hyph) Unless Deborah Joyce Holman, Yara Dulac Gisler Swiss artists Deborah Joyce Holman and Yara Dulac Gisler open their video triptych Unless (2021) with a pair of t
- (genuine) Each talon appears to squeeze a swollen orb of blown glass, imbuing the fixtures with eerie sensuality.

### thermostat  [general] 총 13 / genuine 1 (8%)
- 분포: capinit 4, cap 5, hyph 1, urlish 2, genuine 1
- (cap) Thermostat – more than just a heat detector Thermostat is based upon the principle of consolidation of different curatorial approaches and standpoints and is in
- (cap) Further details on the Thermostat program can be found atwww.project-thermostat.eu
- (genuine) Cybernetics explains, for example, how a thermostat maintains a consistent temperature by responding to environmental conditions (the air temperature in a room)

### thrones  [general] 총 13 / genuine 1 (8%)
- 분포: cap 12, genuine 1
- (cap) “To make your veins big.” She reminds me of a character from Game of Thrones.
- (cap) To describe someone as possessing ‘a Burne-Jones look’ is to conjure up a vision of a thin, pale youth with a dreamy expression: it is an androgynous type of be
- (genuine) Arise, children of the weedland, proletariat of the plant kingdom, and topple the thrones of the nobler horticultural flora, chop off their hypercivilized, hybr

### saint  [general] 총 1712 / genuine 133 (8%)
- 분포: trunc 5, allcaps 16, capinit 36, cap 1502, hyph 2, urlish 17, noneng 1, genuine 133
- (cap) Tallentire is now a professor and tutor at Central Saint Martins College of Art and Design, as well as a convenor of the research project
- (cap) I remember the Film and Video Department at [Central] Saint Martins in the late 1980s and 90s, actively going into schools in the wider city, to look for studen
- (genuine) Norman is a warm-heartednudnik(pest), who is also ahondler(hustler), aluftmensch(dreamer), and, ultimately, alamed-vovnik(secret saint).
- (genuine) The patron saint of the exhibition is Carlo Acutis, the “internet saint” proclaimed by the Catholic Church.

### pentagon  [general] 총 90 / genuine 7 (8%)
- 분포: trunc 2, cap 80, urlish 1, genuine 7
- (cap) How about: college kid wants to steal the very latest computer games via the telephone line and instead hacks into the computer system at the Pentagon.
- (cap) The megabrain at the Pentagon realizes that it's all been just a simulation game, the rockets are deactivated.
- (genuine) Or a point can become three leading to a triangle, or four to a square, five to a pentagon, hexagon, octagon, and so on—it’s endless.
- (genuine) The latter calls the interval of the major third "male", because it is related to the figure of the pentagon which has odd angles and is therefore–according to 

### east  [general] 총 4516 / genuine 356 (8%)
- 분포: trunc 6, allcaps 23, capinit 28, cap 4014, hyph 59, urlish 29, noneng 1, genuine 356
- (cap) The first was directed towards Latin America and the Caribbean and the second also included Asia, Africa and the Middle East.
- (cap) (1995/6, miniDV), part of Zorn’s Werkleitz programme, which depicted parts of the East German landscape that had been affected by mining and chemical production
- (genuine) As the veteran East Ender noted, the initiative wasn’t just about bringing people out east but about bringing part of the east to the west by extending opening 
- (genuine) As the veteran East Ender noted, the initiative wasn’t just about bringing people out east but about bringing part of the east to the west by extending opening 

### peck  [general] 총 87 / genuine 7 (8%)
- 분포: capinit 12, cap 68, genuine 7
- (cap) Highlights of their collection on view include paintings by Ammi Phillips, Sheldon Peck, and John Brewster Jr.
- (cap) In 50 Minus 1 Ute Meta Bauer and Ana Salazar have selected seven moving-image artworks that dwell on systemic violence and oppression—by Alain Resnais and Margu
- (genuine) If the girl wants to peck the dick off the guard and calls on the birds to help her, she isn’t powerful enough to simply call the birds.
- (genuine) The chickens fight each other in the garden, peck at the legs of the dead, strewn across the slabs.

### almanac  [general] 총 161 / genuine 13 (8%)
- 분포: allcaps 27, capinit 12, cap 105, hyph 1, urlish 3, genuine 13
- (cap) In: Leonardo Electronic Almanac, Vol.
- (cap) He is director of [techne] New Media + Digital Arts and his work has been featured on Alt-X, Ars Electronica 99, Ctheory, Body & Society, Leonardo Electronic Al
- (genuine) Compiled in an “almanac of darkness”, these letters catalogue the various ways — religious, spiritual and poetic — in which violence can be resisted.
- (genuine) In fact, this issue of Bracket (an annual almanac that defines itself as at “the junction of architecture, environment and digital culture”) is dedicated to the

### gristle  [general] 총 37 / genuine 3 (8%)
- 분포: cap 34, genuine 3
- (cap) Although it seems ages since Throbbling Gristle and those vehement sessions of post-punk took place, the musical output of this unique and extreme performer rem
- (cap) In a typically agile move, the show was to be both the culmination and death of COUM’s art-related activities – the duo relaunched themselves at the opening as 
- (genuine) It vivifies detail in the rubbered gristle of a dildo; in the viscid gloss of a heel; in the pert nugget of a nipple; in the chalky diacritics of scars; in the 
- (genuine) I think about a chicken’s neck congealing like that, healing, creating layers of new skin and bone, and muscle and gristle, and feathers and leaky eyes, till th

### pueblo  [general] 총 37 / genuine 3 (8%)
- 분포: cap 31, hyph 1, urlish 1, noneng 1, genuine 3
- (cap) 1983 in Santa Fe, New Mexico; Lives/works at Santa Clara Pueblo
- (cap) Writing on the documentation of Fragments, Verwoert comments on two found images of women at work, not Pueblo women painting, but others, immersed in the seemin
- (genuine) Instead, this landscape evokes the enfolding warmth of the pueblo and its peoples, suggesting its continuing importance in Johnstone’s work.
- (genuine) One of the most notable and famous piece by the duo is the 1977 “Agarrando el pueblo” (“Vampires of Poverty”), manifesto of the movement called Pornomiseria, i.

### west  [general] 총 5037 / genuine 413 (8%)
- 분포: trunc 5, allcaps 60, capinit 79, cap 4379, hyph 52, urlish 49, genuine 413
- (cap) This did not mean the end of the West.
- (cap) Decolonial thinking strives to delink itself from the imposed dichotomies articulated in the West, namely the knower and the known, the subject and the object, 
- (genuine) The coming competition for a new common sense of what the world means and how it is organised, which actions now taking place in north Africa and west Asia pred
- (genuine) Sam Auinger/Rudolf Heidebrecht/Just Merrit The wind blows mainly from the west through the "Danube Gate" of Linz.

### serpentine  [general] 총 692 / genuine 57 (8%)
- 분포: allcaps 6, capinit 10, cap 618, urlish 1, genuine 57
- (cap) The Japanese architect is known for his design of Tokyo’s Musashino Art University Museum and Library; in 2013, London’s Serpentine Galleries tapped him for its
- (cap) As he told Hans Ulrich Obrist, the Serpentine Gallery’s artistic director, in a recent interview: “In 1963 my neon works were provocative, vulgar and unsaleable
- (genuine) And so even as we’re being trained to adhere to these serpentine haptic routines, we will need to forget—if only in our muscles—having ever swiped otherwise.
- (genuine) Candles have been a mainstay in Akashi’s work since 2012, sometimes evoked in serpentine bronze shapes that preserve the contours of the igneous substance that 

### phoenix  [general] 총 208 / genuine 17 (8%)
- 분포: allcaps 3, capinit 6, cap 178, hyph 2, urlish 2, genuine 17
- (cap) Made up of three hundred works by various artists including Ana Mendieta, Hélio Oiticia, and Lygia Clark, the collection has been exhibited at the Art Institute
- (cap) This year she premiered Water Sky Gardenat the Vancouver Olympic Winter Games, and she completed 2009′s largest US public art commission,Her Secret is Patience,
- (genuine) This much we do know: Migrating Forms, the phoenix that rose from the ashes of the New York Underground FilmFestival, is now in its fifth installment—and its fi
- (genuine) But as a phoenix, it systematically arises from its own ashes, finding new embodiments, followers and practisers – in a word, “re-inventing” itself.

### pies  [general] 총 134 / genuine 11 (8%)
- 분포: trunc 108, cap 9, urlish 6, genuine 11
- (trunc) Paintings by Alberto Burri, Lee Bontecou, Lucio Fontana, Piero Manzoni, Manolo Millares and Antoni Tàpies will also be on display.
- (trunc) One of the princi­ pies of the group is non-specialization-we want to be open for everybody and everything.
- (genuine) The pastries change frequently, depending on what they’ve cooked that day – if you’re lucky, you’ll get to try their apple pies or their pavlova with berries.
- (genuine) It appears that Pantonehas fingers in many pies lately.

### lord  [general] 총 338 / genuine 28 (8%)
- 분포: allcaps 2, capinit 16, cap 290, urlish 2, genuine 28
- (cap) Board chair Lord Browne said, “The trustees and I know that Maria has the vision, drive and stature to lead Tate into its next phase of development.
- (cap) Wilde’s imprisonment led to his last great works:De Profundis, an extended letter to his lover Lord Alfred Douglas written by Wilde in his prison cell, and "The
- (genuine) Kubrick, he claims, was so pleased with his performance that he apparently expanded the importance of his role—that of Bullingdon, the young lord who brings dow
- (genuine) In other words, they will be able to experience the inspirations and expirations of nature that tend to be veiled by the absurd arrogance of man to consider him

### cod  [general] 총 72 / genuine 6 (8%)
- 분포: trunc 2, allcaps 1, capinit 12, cap 50, urlish 1, genuine 6
- (cap) The seas are empty [once-abundant species such as Atlantic Cod are threatened with extinction], but the majority of highly educated, computer-networked artists,
- (cap) The power and speed of the clashing bodies resonate with the Cod.Act, André Décosterd (CH), Michel Décosterd (CH) Uperqt elevated vocal pulsations of the fans.
- (genuine) , a truck equipped to distribute a small selection of artificial substitutes for foods at risk of extinction, showed into three menus: cod, peanut butter and ch
- (genuine) , a truck equipped to distribute a small selection of artificial substitutes for foods at risk of extinction, showed into three menus: cod, peanut butter and ch

### bantam  [general] 총 12 / genuine 1 (8%)
- 분포: capinit 2, cap 9, genuine 1
- (cap) 7 Among Cage's most famous aphorisms, these were quoted in the mixed-means "bible" of the middle 1960s, Marshall McLuhan and Quentin Fiore's The Medium is the M
- (cap) Tom Wolfe, “What If He Is Right?,” in The Pump House Gang(New York: Bantam, 1999), 127–28.
- (genuine) Zittel’s letters, photographs, and drawings shows the gradual design process from cages for bantam breeding to forms of human domestic furniture.

### episcopal  [general] 총 12 / genuine 1 (8%)
- 분포: cap 11, genuine 1
- (cap) She was born in Jiangxi, China, in 1920 to Episcopal missionaries.
- (cap) The quake also buckled the capital’s Episcopal Holy Trinity Cathedral and ruined its large colorful murals by Haiti’s top artists, including a depiction of Chri
- (genuine) It was on a day off from my choral duties at the Cathedral that my episcopal father took me to Cookham, Stanley’s hometown, where the artist had set many of his

### excellency  [general] 총 12 / genuine 1 (8%)
- 분포: cap 11, genuine 1
- (cap) The exhibition is organised with the kind support of Her Excellency Sheikha Hoor Al Qasimi, Sharjah.
- (cap) The Canadian ambassador, His Excellency Marc Lortie, announced the presence of another Canadian artist, Michael Snow, but he forgot to mention that Canuck paint
- (genuine) “We are grateful for the high level of dedication and expertise that Al-Khudairi has contributed to the development and successful inauguration of Mathaf,” stat

### satanism  [general] 총 12 / genuine 1 (8%)
- 분포: cap 8, urlish 3, genuine 1
- (cap) pushing young people into Satanism
- (cap) pushing young people into Satanism
- (genuine) Later, after Nathan performs aSalò-esque shit-eating ritual devised by their imaginary six-year-old son, although they’re really just enjoying some chocolate, s

### eyed  [general] 총 297 / genuine 25 (8%)
- 분포: trunc 1, allcaps 1, cap 10, hyph 260, genuine 25
- (hyph) "The Living Meme is cross-bred with the rhetorie of (strong) Artificial Life and Artificial lntelligenee and the wide-eyed notion of global networks achieving b
- (hyph) A name, my keys, where I parked, constantly.” But do you remember being a sticky wild-eyed kid?
- (genuine) At the Modern Institute booth, Warhol Foundation president Joel Wachs, an active collector of apartment-size art, eyed two paintings by Haley Tomkins.
- (genuine) A recent demonstration left a small kiosk and three buses burned, and the cops eyed everyone who was visibly under fifty with maximum suspicion.

### bode  [general] 총 118 / genuine 10 (8%)
- 분포: trunc 1, allcaps 1, capinit 9, cap 97, genuine 10
- (cap) Founded by Arnold Bode, Documenta has taken place every five years in Kassel since 1955.
- (cap) It’s easy to forget: Arnold Bode’s documenta opened in 1955 with shrapnel outside the lawn of Kassel’s Fridericianum; he founded the mega-exhibition (internatio
- (genuine) The future does not bode well for globalization.
- (genuine) Late Friday night, Andrea Lissoni presented a lineup of three strong video works that bode well for his upcoming directorship at Munich’s Haus Der Kunst.

### neolithic  [general] 총 82 / genuine 7 (8%)
- 분포: capinit 4, cap 70, hyph 1, genuine 7
- (cap) From matriarchy 6,000 years ago to the idealization of women in Neolithic symbols and Queen Teuta, the role of women in society diminished—almost sinking into o
- (cap) In 2015, Italian architect and designer Andrea Branzi began exhibiting transparent models that propose a kind of Neolithic present, mingling ancient and contemp
- (genuine) The project focuses on a collection of 9,000-year-old neolithic masks excavated in the West Bank and the surrounding areas.
- (genuine) A Cornish neolithic chamber tomb, Chûn Quoit, believed to have been built around 2400 BC, provided inspiration for Single Form (Chûn Quoit)1961.

### git  [general] 총 59 / genuine 5 (8%)
- 분포: capinit 1, cap 52, urlish 1, genuine 5
- (cap) MovesMapper on Git Hub|Moves.app for iOS|Nicholas Felton
- (cap) Die Bereitstellung von Mustercodes und erweiterten Datennutzungsfunktionen über den Social-Coding-Dienst Git Hub ermöglichte überdies Sekundärkreationen durch P
- (genuine) The development took place in NY, and it is deployed remotely through the git DVCS.
- (genuine) We do not take credit for an entire work; instead, we live with many, by git pulls and repositories.

### sous  [general] 총 59 / genuine 5 (8%)
- 분포: capinit 11, cap 22, hyph 15, noneng 6, genuine 5
- (cap) In Yi’s fall 2011 exhibition “Sous Vide” at 47 Canal, we found drips of olive oil, a liquid whose color (at least on the screen) almost exactly matched that of 
- (cap) There are strong references to the historical avant garde running through the ten tracks of “Sous Les Etoiles”, Kiko C.
- (genuine) July 8, 7pmBar sous le toit: performative lecture by students of Kunsthochschule Mainz
- (genuine) An engraving from 1843, part of a series entitled Les français sous la révolution, depicts The Breaker of Imagesas a snarling grotesque.

### secession  [general] 총 405 / genuine 35 (9%)
- 분포: capinit 3, cap 360, urlish 5, noneng 2, genuine 35
- (cap) and abroad including the Moderna Museet, Malmö; Mo MA PS1, New York; The Center for Contemporary Art, Tel Aviv; the Kunstverein Hamburg; and Secession, Vienna.
- (cap) The artist’s solo exhibitions include shows at Le Consortium, Dijon, 1997; Weiner Secession, Vienna, 1999; Museo Serralves, Porto, 1999; Centre Pompidou, Paris,
- (genuine) Cinema seems more or less still in the mainstream, as if it never had a “secession” of modern or modernist artists against that mainstream.
- (genuine) At secession, Vienna until February 20, 2022

### polish  [general] 총 1058 / genuine 92 (9%)
- 분포: trunc 1, capinit 19, cap 925, hyph 8, urlish 13, genuine 92
- (cap) Muir measured the treasures adorning the house, pausing in front of a Piotr Janas painting and waxing ecstatic on the Polish artist, who, in his opinion, is sor
- (cap) In the main section, Piktogram/BLA displayed work by Polish artist Knaf and his various associations, collectives, and ephemera like beautiful broken shards of 
- (genuine) Of course, people-watching from the sidewalk is not without its appeal in this neck of the woods, where passersby tend to have a degree of polish observed less 
- (genuine) On Tuesday, Delphine Arnault and Weditor Stefano Tonchi welcomed guests to the opening of a Reyle-designed Dior pop-up store, where you could buy accessories (s

### musics  [general] 총 242 / genuine 21 (9%)
- 분포: allcaps 10, cap 203, urlish 6, noneng 2, genuine 21
- (cap) Hybrid Art and Digital Musics & Sound Art will be back in 2015.
- (cap) The categories have changed and expanded as things have progressed - now, in 2004, there are seven categories: Computer AnimationlVisual Effects, Dig ital Music
- (genuine) The urge to discover new musics, to pioneer the exploration of fresh musical realms, to undertake daring tonal experiments is still undiminished.
- (genuine) A line could be traced from this Cockneyfied shock of the new to all the musics that bastardized and made willfully tasteless the sounds of New York and Chicago

### coop  [general] 총 92 / genuine 8 (9%)
- 분포: trunc 5, allcaps 7, capinit 7, cap 48, urlish 17, genuine 8
- (cap) C’s began and we are left, willingly or not, with that bad Coop.
- (cap) Smart Coop · http://www.smart.coop Freelancers are a new normal in today’s knowledge economy.
- (genuine) As a boy, he would play with the hens around his house in the country, later destroyed by the conflict, and imi- tate their clucking; as an adult, he began draw
- (genuine) the medium as a construction material on coop himmelb(l)au KATHARINA GSÖLLPOINTNER Heart Space, 1969 Astroballoon Through a transparent shell — like an enlarged

### gob  [general] 총 23 / genuine 2 (9%)
- 분포: capinit 6, cap 12, hyph 1, urlish 2, genuine 2
- (cap) Here it becomes clear that seemingly anything is possible, as each individual steals and samples material from other peoples homepages, websites and media, enco
- (cap) Back in June, in the middle of Berlin’s cultural lockdown, when all the theatres were closed,Gob Squadpresented Show Me A Good Timeas an ambitious 12 hour lives
- (genuine) To exploit its most notorious image, the film is a gob of spittle in the face of what today passes for adversarial art and politics.
- (genuine) As I greedily reached for more melted Gruyère from one of the blobs that had landed on the base, I almost got splattered with a gob on my sleeve, much to the am

### gorgon  [general] 총 23 / genuine 2 (9%)
- 분포: cap 21, genuine 2
- (cap) Equally striking, both for nineteenth-century and contemporary audiences, is the distinctive eye with which the artist mediated between classical mythology and 
- (cap) According to this story, the priestess Medusa (whose name, says the poet Hesiod, means “I rule,” making her a queen) was one of three Gorgon daughters of the se
- (genuine) In Luiza Teixeira de Freitas’s “Between 58 and 131 infinitely” at Galerie Martin Janda, the literary reared its gorgon head once again.
- (genuine) The “Snakelock” motif draws on Williams’ interest in the snake-haired gorgon Medusa, the head of which Perseus used to turn the sea monster Cetus to stone, and 

### ups  [general] 총 725 / genuine 64 (9%)
- 분포: trunc 3, allcaps 3, cap 9, hyph 640, urlish 6, genuine 64
- (hyph) Later Van GoghTV included television in similar set-ups, making use of the increasing accessibility of television equipment and satellites.
- (hyph) As a fund of databases grows, and it looks as if software is growing with it both in variety and capability, the desire to involve them in net.radio set-ups of 
- (genuine) Despite a number of ups and downs, we were able to complete the construction of our bamboo frame one step at a time and in the process create a group dynamic th
- (genuine) Once in town, my target was the Parrish Art Museum’s Midsummer Party, the institution’s last annual fundraiser before it ups sticks to a brand new Herzog & de M

### lino  [general] 총 34 / genuine 3 (9%)
- 분포: trunc 1, capinit 9, cap 19, hyph 1, noneng 1, genuine 3
- (cap) Credits: Created by Matteo Zamagni, Soundtrack by TSVI / 3D Production : Lino Sabia, Lorenzo Depascalis, Claudio Giambusso, Matteo Zamagni / Editing, Compositin
- (cap) Linus Baumeler invites Elischa Heller, Cyril Tyrone Hübscher and Lino Meister to contribute to the space by means of sound, sculpture and sensorial works.
- (genuine) However, for this piece Brazelton has carved the outline of a human head into the material, akin to how one would carve a lino cut.
- (genuine) You will take your own individual approach to the subject, supported and inspired by our team of world-renowned artists and thinkers.MA Printmakingallows studen

### vassal  [general] 총 34 / genuine 3 (9%)
- 분포: allcaps 1, cap 30, genuine 3
- (cap) 3pm The Imaginaries of Transformation: Anne Lacaton & Jean-Philippe Vassal and Frédéric DruotKarine Dana20 min
- (cap) Anne Lacaton & Jean-Philippe Vassal and Frederic Druot (Paris, France)
- (genuine) He didn’t “grant” permission, as if to a vassal or like a member of the clergy.
- (genuine) is a vassal state in the Empire of Plants.

### beavers  [general] 총 79 / genuine 7 (9%)
- 분포: capinit 8, cap 64, genuine 7
- (cap) With him was his life partner Robert Beavers, himself a burgeoning filmmaker and nineteen at the time.
- (cap) This would take years, and in a further obstacle, Markopoulos’s cement splices began disintegrating after a decade or two, so Beavers (alongside, more recently,
- (genuine) Culture, poetry, dance: these are not activities limited to humans, and I would extend our field of “art” to include the patterns of plants and peacocks, the da
- (genuine) Within this surreal landscape, golden beavers and mice gather amidst a tangled mass of branches.

### university  [general] 총 21814 / genuine 1968 (9%)
- 분포: trunc 77, allcaps 17, capinit 223, cap 19288, hyph 42, urlish 198, noneng 1, genuine 1968
- (cap) I had graduated from Douglass College, the women’s college at Rutgers University, in 1968, and gone on to graduate school at Hunter College in New York City, wh
- (cap) At some point, roughly 1971, Lucy took myself, Jackie Winsor, Charles Simonds and one other artist to Virginia Commonwealth University, where we spent a few day
- (genuine) In the current situation in Europe, human beings who are identified as immigrants or refugees not only do not have room in the media or university to make their
- (genuine) IT:U is a young public technical university ­dedicated to digital transformation, focusing on interdisciplinary research and project-based, personalized learnin

### byzantine  [general] 총 111 / genuine 10 (9%)
- 분포: capinit 1, cap 100, genuine 10
- (cap) What was left was the agricultural product, parchment, on which monks were constrained to copy the censored Christian version of what was contained on papyrus, 
- (cap) Venues:Alatza Imaret, Archaeological Museum of Thessaloniki, Bey Hamam, Museum of Byzantine Culture, Jeni Tzami, Eptapyrgio, Casa Bianca, Contemporary Art Centr
- (genuine) El Estudiante, written and directed by Santiago Mitre (who has cowritten scripts with Trapero), centers on a twenty-something newcomer to Buenos Aires who becom
- (genuine) ∗This is exemplified by the byzantine argument presented by al-Azhar, Egypt’s and the Arab world’s highest Sunni authority, in December 2014, which refrained fr

### shaker  [general] 총 89 / genuine 8 (9%)
- 분포: capinit 3, cap 75, hyph 1, urlish 2, genuine 8
- (cap) Curated by Rotana Shaker, the exhibition spans the indoor galleries and outdoor courtyards and brings together new commissions and existing works drawn from the
- (cap) Next came images of a Shaker settlement (the founder of the Shakers, Anne Lee, emigrated to America from Manchester).
- (genuine) Historic and contemporary photography of Shaker architecture is paired with objects such as a shaker dwelling staircase and a four-metre-long bench to reveal th
- (genuine) Home and mother/Wheres a cocktail shaker, Ben, heres plenty of cracked ice’.

### ration  [general] 총 110 / genuine 10 (9%)
- 분포: trunc 88, allcaps 1, cap 9, urlish 2, genuine 10
- (trunc) Together, the artists multiply the sites of resistance for their/our muscles.Press file availablehere.The CAC Brétigny is a cultural establishment of Coeur d’Es
- (trunc) A photo by Moussa Ag Assarid, writer and representative of the Mouvement National de Libération de l’Azawad, or MNLA (National Liberation Movement of Azawad), s
- (genuine) Credits: Felix Luque (Author), Iñigo Bilbao (Technical 3D design), Vincent Evrard (Arduino programming), Production by “secteur arts numériques, Fédération W
- (genuine) Even national health systems might choose to ration the provision of care on the basis of genetic propensity for disease, especially to families at risk for bea

### mesa  [general] 총 77 / genuine 7 (9%)
- 분포: allcaps 2, capinit 2, cap 62, noneng 4, genuine 7
- (cap) Trevor Paglen, Lacrosse / ONYX II Radar Imaging Reconnaissance Sattelite Passing Through Draco (USA 69) , 2007 and Threat Emitter Halligan Mesa, NV , 2012 Rober
- (cap) Plan:b Arquitectos / Felipe Mesa & Federico Mesa (Medellin, Colombia)
- (genuine) So in 1967 she left New York, roamed in a camper van for a year and a half, then settled atop a mesa near Cuba, New Mexico.
- (genuine) Krazy steals the portrait, runs off across the mesa and eventually hangs it over the jailhouse window in such a way that it looks as if it is the “real” Ignatz.

### gunning  [general] 총 55 / genuine 5 (9%)
- 분포: capinit 1, cap 48, hyph 1, genuine 5
- (cap) [2] See Tom Gunning, 1986.
- (cap) Participating artists include: Anna Barriball, Simon Bill, Ian Dawson, Tacita Dean, Ceal Floyer, Anya Gallaccio, Lucy Gunning, Chantal Joffe, Margherita Manzell
- (genuine) (people’s strike) and ending with government forces gunning down 20 protesters.
- (genuine) According to Sophia Kishkovsky of the Art Newspaper, the gunning down of a Russian fighter jet on November 24 that appeared to pass through Turkish airspace whi

### mamma  [general] 총 33 / genuine 3 (9%)
- 분포: capinit 4, cap 25, noneng 1, genuine 3
- (cap) Seven artists were invited to serve on the biennial’s curatorial team: Alejandro Cesarco, Antonio Ballester, Claudia Fontes, Karin Mamma Andersson, Sofia Borges
- (cap) They will be curated by Alejandro Cesarco, Antonio Ballester Moreno, Claudia Fontes, Mamma Andersson, Sofia Borges, Waltércio Caldas, and Wura-Natasha Ogunji.
- (genuine) A program with many alternatives at each step, whose pain and pleasure systems a re arranged to produce a pleasure signal on hearing the word "good" and a pain 
- (genuine) I am very fond of La mamma di Boccioni , for example, in bronze, that originated with a version in mint-flavoured candy, to which I added two bowling balls for 

### catchers  [general] 총 11 / genuine 1 (9%)
- 분포: cap 5, hyph 3, urlish 2, genuine 1
- (cap) ‘ for the 2005 Boston Cyberarts Festival and subsequently as ‘Culture Catchers’ at the gallery G-A-S-P, the artwork made by Michael Sheridan is a sound installa
- (cap) Distant Views / Culture Catchers it’s a like a wall of sound made by an international stream of consciousness.
- (genuine) Though these seem like typical Sci-Fi images, on closer examination unlikely characters are revealed such as log cabins, wild animals, dream catchers, house pla

### esters  [general] 총 11 / genuine 1 (9%)
- 분포: cap 10, genuine 1
- (cap) shifts the viewer’s perception of Haus Esters, built between 1927 and 1930 by the internationally renowned architect Ludwig Mies van der Rohe.
- (cap) The artist’s work is therefore ideally suited to Haus Esters by Mies van der Rohe.
- (genuine) As listed in Table 1, the general classes of solvents that had a useful effect on the ink included alcohols, ethers, esters and ketones.

### kilowatt  [general] 총 11 / genuine 1 (9%)
- 분포: allcaps 2, cap 1, hyph 7, genuine 1
- (hyph) During the oil crisis in 1973, inhabitants of one of the first sweat equity co-ops, located at 519 E 11th Street, installed a landmark two-kilowatt wind turbine
- (hyph) It is common for energy to be expressed in kilowatt-hours.
- (genuine) While this can be quantified in watts, joules or kilowatt hours, these figures can be abstract.

### mitten  [general] 총 11 / genuine 1 (9%)
- 분포: capinit 1, noneng 9, genuine 1
- (noneng) wäre, ein 3.500 Quadratmeter großes Gelände mitten im Zentrum von Madrid abgezäunt zu lassen.
- (noneng) Wir befinden uns mitten in einer Revolution, die verspricht, die Herstellung von Dingen für immer zu verändern.
- (genuine) A Hula Hoop packet dated August 1986 found in the Thames; a balloon fragment inside a mitten crab’s stomach.

### speedway  [general] 총 11 / genuine 1 (9%)
- 분포: cap 10, genuine 1
- (cap) Ingrid Calame, meanwhile, needed a hazmat suit to escape the dust that her commissioned, graffiti-like wall painting,Indianapolis Motor Speedway, Pit #4, #9, #7
- (cap) Here the relief corps sets up shop for three days at the vast Bristol Motor Speedway in Pikesville, Kentucky, where thousands of people who haven’t seen a docto
- (genuine) Staged in California as a daylong racing event at Willow Springs speedway, The Snowball was ultimately destined for the 2000 Venice Biennale and Rhoades’ collab

### tapper  [general] 총 11 / genuine 1 (9%)
- 분포: capinit 2, cap 8, genuine 1
- (cap) All data was gathered using Tapper – a small OSX app logging application usage written by Dean McNameeand later visualized by Marcin usingPlaskenvironment.
- (cap) These are naïve and/or mixed perspectival geometries (cf.Tapper,Zoo Keeper, et al.) that have recently been exploited to brilliant effect in Polytron’s visual d
- (genuine) To be sure, the story has a conveniently “universal” ring: Cisco (Bishop Blay) is an underpaid rubber-tree tapper who, after a failed labor strike, leaves for A

### unchained  [general] 총 11 / genuine 1 (9%)
- 분포: cap 9, urlish 1, genuine 1
- (cap) Performance: Unchained Melody December 12, 7pm
- (cap) Alice Unchained CNMAT is dedicated to multidisciplinary research and the creative use of sound, linking the concert hall to the laboratory.
- (genuine) From Gallucci, on her knees and with ponytailed naïveté, we hear of the artist, the activist, and the philanthropist, fickle archetypes unchained from any indiv

### yep  [general] 총 11 / genuine 1 (9%)
- 분포: capinit 1, cap 9, genuine 1
- (cap) 1 The numbers reported come from Robert Bickers and Ray Yep, “Studying the 1967 Riots: An Overdue Project,” in May Days in Hong Kong: Riot and Emergency in 1967
- (cap) Robert Bickers and Ray Yep (Hong Kong: Hong Kong University Press, 2009), 1.
- (genuine) Just after this painting I bought a Polish book on art history, I became fond of a few early stone sculptures and felt that I had to paint at least one of them,

### cobra  [general] 총 119 / genuine 11 (9%)
- 분포: allcaps 8, capinit 3, cap 94, hyph 1, urlish 2, genuine 11
- (cap) With the exhibitions of Bosmans and Wang, Xander Karskens concludes his curatorship at the museum and takes up his position as Artistic Director of the Cobra mu
- (cap) Organized by the Museum of Contemporary Canadian Art, Toronto and the Cobra Museum, Amsterdam.
- (genuine) Well, that, and Debra Paget’s cobra dance from Lang’sIndian Epic.
- (genuine) There were still plenty of bottles of cobra venom left in the bar set up by artist Carl Michael von Hausswolff, so I made a tentative toast with curator Power E

### musk  [general] 총 76 / genuine 7 (9%)
- 분포: capinit 1, cap 65, hyph 2, urlish 1, genuine 7
- (cap) How would the world look if Elon Musk were right?
- (cap) But which functions are worth improving, if we shift our concept of the human condition past the biological realm in order to stay relevant as humans, as Elon M
- (genuine) I imagined the bikes carefully drawn by Tom of Finland, with muscular men pressed against them and each other, and smelled the musk of a hundred sex parties mix
- (genuine) Though their flounce and curve have a pornography of color, flowers as a metaphor can be easily read as safe, sanitized stand-ins for the real musk and squelch 

### robins  [general] 총 65 / genuine 6 (9%)
- 분포: capinit 6, cap 51, urlish 2, genuine 6
- (cap) “I own 70 percent of the Design District,” said Craig Robins as he led a pre-Basel hard-hat tour of the district.
- (cap) This legacy began in the 1990s, when Robins bought up many of the low-lying industrial buildings and invited artists to use some as studio spaces, free of charg
- (genuine) Solo recordings of chiffchaffs, great tits, redstarts, robins, thrushes, and entire dawn choruses were used to train two neural networks (a Generative Adversari
- (genuine) On the mornings that had once throbbed with the dawn chorus of robins, catbirds, doves, jays, wrens, and scores of other bird voices there was now no sound; onl

### prince  [general] 총 841 / genuine 78 (9%)
- 분포: allcaps 5, capinit 49, cap 696, hyph 1, urlish 11, noneng 1, genuine 78
- (cap) But many missed the absent and now earlier greats of the collection: the Auerbachs, Bacons, Oehlers, Richters, Kippenbergers, and Freuds are left out in favor o
- (cap) Richard Prince is an artist based in upstate New York.
- (genuine) Proletarian allegiances aside, Visconti was not known to be a particularly fraternal fellow—in playing The Leopard’s prince, Lancaster famously studied and imit
- (genuine) Ludwig has none of the prince’s ineradicable dignity, though he does have his own sense of style.

### frost  [general] 총 162 / genuine 15 (9%)
- 분포: capinit 9, cap 134, hyph 3, urlish 1, genuine 15
- (cap) Lynch and Frost, also reflexively, write arcs that call to the superfan’s conspiratorial instinct.
- (cap) Lynch and Frost wrote the show’s four-hundred-page script in a couple months and started production before it seemed plausible that Trump would win.
- (genuine) Slides of frost patterns, for example, can be made from a solution of hyposulphate or urea, put on the film (or on thin glass).
- (genuine) Værslev would systematically experiment by leaving works in progress out in the snow and subject paint and chemical products to frost to observe their alteratio

### ding  [general] 총 151 / genuine 14 (9%)
- 분포: trunc 3, allcaps 6, capinit 13, cap 108, hyph 2, urlish 3, noneng 2, genuine 14
- (cap) Works by Isabelle Cornaro at Hannah Hoffman; Julian Charrière at Dittrich & Schlechtriem; Petr Davydtchenko at Harlan Levey; and Emilie Ding at Samy Abraham, am
- (cap) Étude Carpeaux, shown as part of Meise’s 2009 solo exhibition “Ding und Körper” (Object and Body) at the Badischer Kunstverein in Karlsruhe, Germany, takes this
- (genuine) Ding ding ding, the box holds a cherry pie.
- (genuine) Ding ding ding, the box holds a cherry pie.

### woof  [general] 총 75 / genuine 7 (9%)
- 분포: allcaps 8, capinit 5, cap 12, urlish 5, noneng 38, genuine 7
- (noneng) Puppies Puppies Woof woof Puppies Puppies woof woof woof, woof woof woof woof woof.
- (noneng) Puppies Puppies Woof woof Puppies Puppies woof woof woof, woof woof woof woof woof.
- (genuine) The cornerstone of this artist’s vision lies in marking and remanipulating the ways in which those bodies warp and woof the curvature of space, transfix the flo
- (genuine) “bau bau” is Italian for “woof woof,” while “Bau” means “building” in German, and also “in construction.” The title of the exhibition, therefore, is both the so

### lumen  [general] 총 54 / genuine 5 (9%)
- 분포: allcaps 2, capinit 2, cap 44, hyph 1, genuine 5
- (cap) He is a recipient of the Major Individual Award from the Arts Council of Northern Ireland, their highest recognition given to leading artists in the country, an
- (cap) , KLERKXMilan, Johann König Berlin, Kosak Hall Vienna, Lumen Travo Amsterdam, Luxardo Rome, maccarone inc.
- (genuine) Nea Geršak’s short animation Na2r_3lumen (na2r_ flow3rs) is a deserving winner of the Young Creatives u10 Prize.
- (genuine) The setup team used included a 5000 lumen projector running from a car via an inverter, and shot with a 5D.

### tinder  [general] 총 54 / genuine 5 (9%)
- 분포: capinit 4, cap 44, hyph 1, genuine 5
- (cap) The multimedia installation Tinder_gun_boys_@ Brussels_ was born from a collection of screenshots of heterosexual men proudly posing with weapons on the dating 
- (cap) The multimedia installation Tinder_gun_boys_@ Brussels_ was born from a collection of screenshots of heterosexual men proudly posing with weapons on the dating 
- (genuine) This method derives from the same fragmented yet flowing social media experience of “reading posts,” “swiping on tinder,” “cruising on #21xoxo Sine Özbilge & Im
- (genuine) They express a classic speculative design through three alleged prototypes: Last Seen, an alarm clock singling a person of interest coming back online; Soul Mat

### mire  [general] 총 53 / genuine 5 (9%)
- 분포: allcaps 1, capinit 2, cap 43, urlish 2, genuine 5
- (cap) Wallace Gallery, New York, USA (Sungrok Choi)–In TransitionbyGalerie Kunstforum Solothurn, Solothurn, Switzerland (Myungjoo Kim)–59th International Venice Bienn
- (cap) On the occasion of Gallery Weekend Berlin 2024, Monika Sprüth and Philomene Magers are pleased to present “territory,” a group show of works by Mire Lee, Liu Yu
- (genuine) Defy Nostalgia Don’t mire yourself in the good old days.
- (genuine) PFYou once said that you ‘wallow in the mire of nostalgia’.

### democrats  [general] 총 42 / genuine 4 (10%)
- 분포: capinit 1, cap 35, hyph 1, urlish 1, genuine 4
- (cap) The irony is slicing, the doom inevitable, the Democrats—unmoved.
- (cap) As was to be expected, Angela Merkel’s Christian Democrats found the reappearance of the “hideous pedestal” a scandal, and accused Flierl of being beholden to E
- (genuine) Then he went on to massacre sixty-nine people at the youth summer camp of the social democrats at Utöya.
- (genuine) These new developments call for a clear attitude from all democrats in the Bundestag, beyond [any] coalition-tactical considerations.

### mutter  [general] 총 42 / genuine 4 (10%)
- 분포: trunc 5, capinit 1, cap 32, genuine 4
- (cap) First results were presented at the FESTIVAL EXPERIMENTELLER MUSIK in Koblenz, Mutter Beethoven Haus, December 1992.
- (cap) That was when I encountered her series Cells1986–2008, which would be the catalyst for my writing Book of Mutter(2017), a text on my mother.
- (genuine) It is possible to mutter, drone, whistle, hum, and all of this will be an expression of the world, and telling a story about it.
- (genuine) Infected by OSS/****, the computer begins to mutter to itself, watched by the users who see their own computer, their virtual home on the desktop, go hay-wire.

### angers  [general] 총 21 / genuine 2 (10%)
- 분포: allcaps 1, cap 18, genuine 2
- (cap) Randa Maroufi is a graduate of the National Institute of Fine Arts, Tetouan, Morocco (2010) and the School of Fine Arts, Angers, France (2013).
- (cap) 1991) Born in Angers, lives between Paris and Athens.Claudia Pagès Rabal(b.
- (genuine) “I am a reflection of my mother’s secret poetry as well as of her hidden angers,” writes the poet Audre Lorde.
- (genuine) With no other technique than what his eyes and hands discover in seeing and painting, he persists in drawing from this world, with its din of history’s glories 

### cantos  [general] 총 21 / genuine 2 (10%)
- 분포: cap 18, noneng 1, genuine 2
- (cap) Through sonic “Cantos,” Akomfrah frames sound as a political archive—registering migrations, atmospheric violence, and imperial fragilities.
- (cap) That was when the drawings on graph paper which made up the Espaços Virtuais: Cantos, Volumes Virtuais(Virtual Spaces: Corners, Virtual Volumes) and Ocupações(O
- (genuine) “Hasta que los cantos broten” encourages entanglement, and the works resist a prescribed order and interact rhizomatically.
- (genuine) Perverse and pluriverse world, multiple verse, cantos of the pluriverse.

### largo  [general] 총 21 / genuine 2 (10%)
- 분포: cap 19, genuine 2
- (cap) Solo show21 July – 5 September 2010Spazio Culturale Antonio Ratti Largo Spallino 1, Como
- (cap) Onthe 20th of July, to celebrate the conclusion of the Advanced Course in Visual Arts,Hans Haacke’s first solo exhibition in Italywill open at the Spazio Cultur
- (genuine) Like the gestures of a conductor, the layout, head turned to the left, then to the right,largo,legato,staccato,andante, executes the notes and cadences for whic
- (genuine) Aurélien Froment “Allegro, largo, triste” Aurélien Froment attempts to bring to the screen the music of Franco Melis, by following its form.

### auburn  [general] 총 52 / genuine 5 (10%)
- 분포: capinit 1, cap 42, hyph 2, urlish 2, genuine 5
- (cap) The Master of Landscape Architecture Program at Auburn University is pleased to announce two fellowship opportunities for 2026–27.
- (cap) Located in one of the most ecologically diverse and culturally rich landscapes in the United States, Auburn’s Master of Landscape Architecture program is the on
- (genuine) All three have donned astonishingly hideous auburn wigs.
- (genuine) The lines are shaped by the memory of sitting for Reynolds: the tinted lip, melting eye, auburn curls, dimpled smile and “veil transparent on the breast of snow

### passe  [general] 총 31 / genuine 3 (10%)
- 분포: allcaps 4, cap 9, hyph 11, urlish 2, noneng 2, genuine 3
- (hyph) Her passe-partout —frames traditionally used to highlight and enclose images—challenge this visual logic.
- (hyph) Jacopo’s paintings become the background landscape of the photographs, a passe-partout, a backdrop from which the shots emerge by contrast and in a strongly ico
- (genuine) Faster than media art theory (in any case largely non-existent) is capable of offering a descrip­ ti on of this phenomenon, a conception of media oriented upon 
- (genuine) He stopped when he had enough material for a book, published as Cette histoire se passe(This Story Happened) in 2011.

### hardy  [general] 총 133 / genuine 13 (10%)
- 분포: allcaps 1, capinit 9, cap 110, genuine 13
- (cap) The hardware engineers ("Hardy Boys", after a popular detective novel series for boys) have also to deal with real beetles, spiders, dust and the likes from the
- (cap) On Sunday, November 15, the artist Ali Cherri paired up with archaeologist Sam Hardy for a powerful discussion of ruins, museums, the destruction of Palmyra, an
- (genuine) There was drinking, and dancing, and ultimately a move by the hardy to a club where a boy band descended from the ceiling on a giant boom, and the ceiling opene
- (genuine) Out on the patio Natalia Slyz, co-owner of SlyzMud Gallery, ecstatically sung the praises of the small, hardy scene of galleries, making me a list of her favori

### frieze  [general] 총 1842 / genuine 183 (10%)
- 분포: allcaps 9, capinit 169, cap 1416, hyph 11, urlish 51, noneng 3, genuine 183
- (cap) The blue-chip gallery has increasingly focused on Asia in recent years, arriving in Seoul in 2017, well ahead of the launch of Frieze Seoul there in 2022.
- (cap) Prior to joining New York University, Lees was head of the Frieze Foundation from 2013 to 2015 and curated Frieze Projects London, mounting over forty large-sca
- (genuine) In both images, the Santa Monica Mountains loom in the distance as overlain line drawings of native vegetation and a Herculean frieze spring from the ground up.
- (genuine) Frieze TalksBringing together leading artists, writers, and cultural commentators,Frieze Talks2015 is programmed by Tom Eccles (Executive Director, Center for C

### renaissance  [general] 총 1368 / genuine 136 (10%)
- 분포: trunc 2, allcaps 9, capinit 15, cap 1182, hyph 9, urlish 14, noneng 1, genuine 136
- (cap) There, of all places, the spirit of the Renaissance could be felt with great intensity and it was difficult not be impressed by the sheer size of the interior s
- (cap) Thus, the Ars Electronica Deep Space was born out of the spirit of the Renaissance, and around it would unfold a complete “rebirth” of the Ars Electronica Cente
- (genuine) A renaissance portrait of a woman is sucked away by a vacuum pump, turning the mouth into an outlet pipe of a bath (Whirlpool, 1999).
- (genuine) Zaha heads the technological renaissance in architecture.”

### creed  [general] 총 182 / genuine 18 (10%)
- 분포: capinit 15, cap 148, urlish 1, genuine 18
- (cap) This particular edition of Saturday Live, subtitled Word Sculpture, focused on the use of language within contemporary art practice and also featured a text-bas
- (cap) All three artists have treated words as sculptural material; Partum scattered words like confetti, Creed generated them through numerical sequences and Andre ar
- (genuine) This work defines Malstaf’s artistic creed because it displays the new technological condition: the motor controls the Bible.
- (genuine) It was enormously influential for a spell among young men looking for a creed, as were the jeremiads of blowhard academic and John Cassavetes biographer Ray Car

### panther  [general] 총 141 / genuine 14 (10%)
- 분포: cap 122, hyph 1, urlish 4, genuine 14
- (cap) The Black Panther Party: Service to the People Programs,
- (cap) Exemplary of this history is the FBI’s Counterintelligence Program (COINTELPRO), which ran from 1956 to 1971 and sought to disrupt, discredit, and destroy indiv
- (genuine) You tiptoe as the echo of the silence feels irreverent, a city where only the soft paws of a panther could own its silence.
- (genuine) A 3D-printed bone structure of what could be both a plebeian stray cat or a dignified panther confounds the relation between appearance and the internal structu

### cations  [general] 총 20 / genuine 2 (10%)
- 분포: trunc 17, urlish 1, genuine 2
- (trunc) Communi­ cations of the ACM, Vol.
- (trunc) Communi­ cations of the ACM, Vol.
- (genuine) Regarding parameter settings, they were all made at rotations of approximately 40 degrees and with spatial magnif1cations slightly less than unity, un­ less oth
- (genuine) Can we envision art that addresses multiple racial, gendered, cultural and even digital identi cations by playing with these constructions?

### deductible  [general] 총 20 / genuine 2 (10%)
- 분포: hyph 18, genuine 2
- (hyph) We have officially moved to Seattle, Washington, USA, where we have begun working with Shunpike, an arts-oriented, non-profit fiscal sponsor, enabling us to rec
- (hyph) Allcontributionsin support of X-TRA are fully tax-deductible.
- (genuine) Tickets The Big Ticket: 1,250 USD (800 USD tax deductible).
- (genuine) The VIP Lounge Ticket: 250 USD (150 USD tax deductible).

### imam  [general] 총 20 / genuine 2 (10%)
- 분포: capinit 1, cap 17, genuine 2
- (cap) Zaynab is the daughter of Fatima and Imam Ali, the sister of martyr Husayn and the granddaughter of the prophet.
- (cap) [9] Zaynab is the daughter of Fatima and Imam Ali, the sister of martyr Husayn and the granddaughter of the prophet.
- (genuine) While the French had developed the train in its colonial expansion, it also gave a way to imam travelers, preachers, and missionaries to move inside very deep a
- (genuine) The imam was standing, reading prayers, inside a tall white alcove cut in the shape of a dome.

### blinder  [general] 총 10 / genuine 1 (10%)
- 분포: cap 8, noneng 1, genuine 1
- (cap) The project will be led by the New York–based architectural firm Beyer Blinder Belle.
- (cap) “At Beyer Blinder Belle, we believe that architecture and design empower neighborhoods and people by connecting them to each other and their everyday built envi
- (genuine) The watchmaker would be blinder than the genetic evolutionary theory suggests to us.

### buss  [general] 총 10 / genuine 1 (10%)
- 분포: capinit 2, cap 6, urlish 1, genuine 1
- (cap) The album opens with the title track “Vulkan”, a piece characterized by the interesting voice of Carmen Buss and a series of delicate, almost ambient treatments
- (cap) Featuring:Cameroon:Perils of Pauline: The Making of a Remake/ // Esther Buss, Moise Mabouson Mabouna, Florian Gass, Dorette Mbogol, Georgette Mbogol, Paul Njoh,
- (genuine) “Why not?” he said, giving the abashed Prince a buss on the cheek.

### falconer  [general] 총 10 / genuine 1 (10%)
- 분포: capinit 2, cap 7, genuine 1
- (cap) Natalya Marconini Falconer reads the city as a constellation of traces, where industrial memory intertwines with familial memory, following a thread that connec
- (cap) Participating artists: Ornella Cardillo, Giuseppe Lo Cascio, Natalya Marconini Falconer and Stella Rochetich.
- (genuine) In falconry, when birds hunt, they create a bridge between the falconer and the skies, getting lost from sight; but they generally return due to the symbiotic r

### gables  [general] 총 10 / genuine 1 (10%)
- 분포: cap 9, genuine 1
- (cap) The opening note in McLuhan and Powers' The Global Village cites Nathaniel Hawthorne's The House of Seven Gables: It is a fact … that, by means of electricity, 
- (cap) If you’re craving a classic Cuban sandwich,Sanguich De Miami(pronounced “Sandwich”) is the spot – or, spots, as the chain has outlets in Little Haiti, Calle Och
- (genuine) At its height, the storm lifted gables and roofs from buildings, flung rafters and entire advertising kiosks through the air, tore trees from the ground, and dr

### godspeed  [general] 총 10 / genuine 1 (10%)
- 분포: allcaps 2, cap 7, genuine 1
- (cap) PP: At least once, for Invisible Boy , the Godspeed piece already existed.
- (cap) Griffin, Toronto singer Mary Margaret O’Hara, and members of Montreal post-rock heavyweights Godspeed You!
- (genuine) I didn’t have nearly enough time to find everything, but with Szymczyk’s colleague Katerina Tselou as my guide I made godspeed for the afternoon.

### kiwi  [general] 총 10 / genuine 1 (10%)
- 분포: cap 8, noneng 1, genuine 1
- (cap) Above – Akio Takamori , 2014 Black Landscape Pot with Kiwi Plant 1 , 2014 Face Painting , 2014 Reggie Lewis , 2014 Blue Rug Still Life , 2014 .
- (cap) So, we’ve freely sampled a couple of international films and a fair few from New Zealand, as a wink to the way that Australians are always trying to take credit
- (genuine) Pei–designed foyer, but it was clear some visitors were hankering for something a little stronger than fresh kiwi juice.

### pap  [general] 총 10 / genuine 1 (10%)
- 분포: trunc 1, allcaps 2, cap 4, urlish 2, genuine 1
- (cap) Errant Bodies Press, Pap/Psc edition, ISBN: 978-098274395, English, 84 pages, 2015, Germany
- (cap) edited by Brandon La Belle, Claudia Martinho – Errant Bodies Press; Pap/Com [book + cd], ISBN: 9780982743904, 304 pages, 2011, English
- (genuine) In the interim, Paul has become a rock star—bigger than Madonna’s pap smear, he’s a hero to a lot of neo-Slackers.

### perm  [general] 총 10 / genuine 1 (10%)
- 분포: allcaps 2, cap 6, noneng 1, genuine 1
- (cap) Her works have been exhibited at venues such as Ars Electronica, National Art Museum of China, Perm Museum of Contemporary Art, and Transmediale.
- (cap) Her works have been exhibited at venues such as Ars Electronica, National Art Museum of China, Perm Museum of Contemporary Art, and Transmediale.
- (genuine) In Untitled (2005), Little catches a lone woman in a sparkling violet dress and bouffant 1980s perm—shoeless but with earrings still in place—somberly nursing a

### sills  [general] 총 10 / genuine 1 (10%)
- 분포: cap 7, urlish 2, genuine 1
- (cap) Kristen Windmuller-Luna as the Sills Family Consulting Curator of African Arts.
- (cap) Kristen Windmuller-Luna, formerly a brilliant student of mine, to the position of the Sills Consulting Curator at the Brooklyn Museum.
- (genuine) Landscapes recomposing worlds on window sills or in shop windows.

### woodsman  [general] 총 10 / genuine 1 (10%)
- 분포: cap 9, genuine 1
- (cap) When the twilight has gone, the song goes, and no songbirds are singing.The Woodsman enters the station, and the secretary moves toward him in an awful trance.
- (cap) The Woodsman begins to crush skulls, killing first the secretary, then the DJ.
- (genuine) Viewed voyeuristically through tangled timothy grasses in a darkling grey-green underbrush, the tiny woodsman Feller prepares to axe a hazelnut.

### dang  [general] 총 18 / genuine 2 (11%)
- 분포: trunc 2, cap 11, hyph 3, genuine 2
- (cap) (aka Dang Khoa Chau) Editing: Hyunji Lee, Ayoung Kim, Chae Yu VFX and motion graphics: Hyunji Lee Unity level design: B.
- (cap) To place a proxy bid or to charge tickets by phone, please contact Jess Dang at (212) 255-5793 ext.
- (genuine) The video game involves the dang er of friendly fire only i n multi-player mode.
- (genuine) Arthur Clarke has described "personalized television safaris" i n which the operator could virtually explore remote environments without dang er or discomfort.

### hallelujah  [general] 총 18 / genuine 2 (11%)
- 분포: capinit 3, cap 11, urlish 2, genuine 2
- (cap) The exception, of course, is “Hallelujah,” which I first heard covered by John Cale and for years believed that he had written it.
- (cap) The worst version of “Hallelujah” I have ever experienced is the VR sing-along by Zach Richter in “Leonard Cohen: A Crack in Everything,” curated by John Zeppet
- (genuine) I am in a procession to the depths, to the deep underground, hallelujah, let it be so.
- (genuine) Mom suggests psychotherapy and, hallelujah, the therapist doesn’t prescribe drugs.

### jive  [general] 총 18 / genuine 2 (11%)
- 분포: cap 15, hyph 1, genuine 2
- (cap) Works from the Barabino Collection;Cosmic Jive.
- (cap) According to Kambalu, his father was the overbearing Jive Talker who used to torture his children with late night drunken philosophical lectures.
- (genuine) News titles out of contexts on sheets of white paper that are often much bigger than the titles themselves suggest an extraction of specificity into an otherwis
- (genuine) Octavia Spencer, as one of the intifadists, is saddled, like most black actors in science-fiction films, with risible pseudo–jive talk (“Hell, yeah!

### leer  [general] 총 18 / genuine 2 (11%)
- 분포: cap 7, urlish 1, noneng 8, genuine 2
- (noneng) Kulturelle Institutionen luden uns ein, das Projekt auszustellen, wobei wir die Gelegenheit nutzten, Workshops zum Mappen leer stehender Häuser mit lokalen Bürg
- (noneng) Gemeinsam wurden „Wohnungs-Safaris“ organisiert, um leer stehende Häuser zu erfassen und Teilnehmern zu erklären, wie der Datenupload über unsere Plattform erfo
- (genuine) Fleshy-lipped figures in outsized turbans leer in sinister cameo roles.
- (genuine) Sarno sometimes shot dialogue scenes that rivaled Welles in depth of field and compactness of composition, in what he called “fore-aft shots”: Whether in a bedr

### aborigines  [general] 총 9 / genuine 1 (11%)
- 분포: cap 6, urlish 2, genuine 1
- (cap) She wrote: “Aborigines are not just the oldest race in Australia; they are the oldest race on the planet.
- (cap) In Australia it might be Brook Andrews, who works on settler colonialism and the violence perpetrated on the Aborigines.
- (genuine) [My comments do] not represent the understanding and appreciation of aborigines that I subsequently acquired through immersion in their world and carry in my he

### achievers  [general] 총 9 / genuine 1 (11%)
- 분포: cap 6, hyph 2, genuine 1
- (cap) Jepchumba has been listed by Forbes as one of the 20 Youngest Power Women in Africa 2012 and by the Guardian as one of Africa’s Top 25 Women Achievers.
- (cap) Jepchumba wurde 2012 von Forbes als eine der „20 ­Youngest Power Women in Africa” und vom Guardian als eine von „Africa’s Top 25 Women Achievers“ ausgezeichnet.
- (genuine) This falls on fertile ground with some people, that one should not feed the weaker ones, the ‘ballast existences,’ but rather promote the high achievers … The A

### ammo  [general] 총 9 / genuine 1 (11%)
- 분포: allcaps 3, cap 3, urlish 2, genuine 1
- (allcaps) The exhibition will be accompanied by a bilingual Distanz-Verlag publication entitled AMMO, which will present widely differing forms of art, advertising, desig
- (allcaps) The painting-installation works Surprised Again and AMMO!
- (genuine) Some are self-evidently screenshots culled from first-person-shooter games, given away by little icons in the corners announcing remaining lives or ammo or high

### arras  [general] 총 9 / genuine 1 (11%)
- 분포: cap 8, genuine 1
- (cap) Holy terror!’.110By mid-September Rheims was a burnt-out shell, the first great cathedral to fall to German guns; Soissons, Arras, Verdun, Louvain and others fo
- (cap) Accompanying the commemoration of the Centenary of the Battle of Arras and the Capture of Vimy Ridge, the exhibition wants to add a crucial poetic voice to the 
- (genuine) One: Stay anonymous, hiding your true name behind an arras of aliases.

### bombardier  [general] 총 9 / genuine 1 (11%)
- 분포: capinit 1, cap 6, urlish 1, genuine 1
- (cap) Ziapour’s concept of painting was based on a socialist understanding of art, as Alice Bombardier discerns from his article in the fourth edition of the magazine
- (cap) See also Alice Bombardier,
- (genuine) One is a captain (Dana Andrews), a war hero bombardier returning to a dead-end job and a party-girl wife (Virginia Mayo) he married on a whim.

### cozier  [general] 총 9 / genuine 1 (11%)
- 분포: cap 7, hyph 1, genuine 1
- (cap) Christopher Cozier (Trinidad & Tobago)
- (cap) Carr is thought to have given the painting to her friend Nell Cozier and her husband in the 1930s.
- (genuine) After a “walking dinner” next to a fiberglass Apatosaurus by Rob Pruitt, those who weren’t feeling prehistoric made their way over to the cozier loft next door.

### filo  [general] 총 9 / genuine 1 (11%)
- 분포: capinit 2, cap 2, hyph 1, noneng 3, genuine 1
- (noneng) There an author of a prototype for a free operation sensencajˆo“, cˆar la nova kodo de lia filo rezultis ne nur en felicˆaj, vojagˆantaj, legantaj kaj edzigˆant
- (noneng) There an author of a prototype for a free operation sensencajˆo“, cˆar la nova kodo de lia filo rezultis ne nur en felicˆaj, vojagˆantaj, legantaj kaj edzigˆant
- (genuine) Equilibrista sul filo (Tightrope Walker on the Wire, 2022–23) advises against rigid junctures in time, displaying the hypnotizing force of a suit-clad funambuli

### lippy  [general] 총 9 / genuine 1 (11%)
- 분포: capinit 2, cap 6, genuine 1
- (cap) Departing from this European appreciation of African art, Irma Stern (1894–1966), the so-called pioneer of South African modernism, and the sculptor Lippy Lipsh
- (cap) In a diary entry of October 26, 1936, Lippy Lipshitz, for example, notes his plan to join Stern on her visit to an Ndebele village ten miles outside of Pretoria
- (genuine) We are looking up towards Tattenham Corner where Emily Davison stepped onto the track and was knocked down by the King’s horse in 1913 – and where, 80 years lat

### lynx  [general] 총 9 / genuine 1 (11%)
- 분포: allcaps 1, cap 5, hyph 2, genuine 1
- (cap) From the original ‘What you see is what you get’ many other acronyms has sprung, like WYSIWYM (what you see is what you mean) used for Lynx, a textual browser o
- (cap) From the original ‘What you see is what you get’ many other acronyms hassprung, like WYSIWYM (what you see is what you mean) used for Lynx, a textual browser or
- (genuine) As we were leaving, a totally face-lifted woman said to thevestiaireattendant: “I’m sorry I lost my ticket, but I have a big white lynx fur coat.” He opened the

### neutrons  [general] 총 9 / genuine 1 (11%)
- 분포: urlish 8, genuine 1
- (urlish) For over a century we’ve known about electrons and the atomic nucleus, which consists of protons and neutrons.
- (urlish) Time spent in van Bender’s universe shows a proclivity for the particles of the atom: protons, electrons, neutrons.
- (genuine) By the time we left, my head was abuzz with talk of protons, neutrons, electrons, and quarks.

### perfections  [general] 총 9 / genuine 1 (11%)
- 분포: cap 6, urlish 2, genuine 1
- (cap) And Amalia Ulman’sExcellences & Perfections2014–5, which takes the form of Instagram posts delivered to her tens of thousands of followers.
- (cap) The double life of Scandalishiousis a precursor to more recent works in which social media is both subject matter and context, such as Amalia Ulman’sExcellences
- (genuine) They are addressed to an audience that, pushed out to the margins by the mainstream’s cartoonish perfections, has been obliged to make their own subcultures – t

### tamarind  [general] 총 9 / genuine 1 (11%)
- 분포: capinit 1, cap 6, noneng 1, genuine 1
- (cap) In 2018, the institution selected artworks by Toyin Ojih Odutola from Albuquerque’s Tamarind Institute and by Ellen Lesperance from Portland’s gallery Adams and
- (cap) June Wayne, founder of the Tamarind Lithography Workshop in Los Angeles and a pioneer of the revival of the fine-art print making in the 1960, has died at the a
- (genuine) Artists use fine brushes made from animal hair, and the cloth canvas is primed with a mixture of chalk and tamarind seed paste, which creates a distinct smoothn

### nautilus  [general] 총 17 / genuine 2 (12%)
- 분포: trunc 2, cap 11, hyph 2, genuine 2
- (cap) The show’s concluding display, a cassette tape of Nautilus Pompilius’s 1985 hit “Goodbye America,” strikes a rather different note of longing: pained disenchant
- (cap) A g.Nautilus EEG cap and specially programmed software enable players to intervene in an image using only their brain waves.
- (genuine) Shaped in plan like a nautilus shell, the Pavilion spirals out from a tapered octagonal column at its centre that supports the dramatic beams of its roof struct
- (genuine) Langdon-Pole’s installation at Auckland gallery Michael Lett’s booth at the fair comprised a new series of works, “Passport,” for which he fused two disparate m

### sigma  [general] 총 17 / genuine 2 (12%)
- 분포: allcaps 1, capinit 2, cap 12, genuine 2
- (cap) Interludes is based on audio recordings from the Sigma Sound Studios Collection at Drexel University’s Audio Archives that the artists were researching for an e
- (cap) Einführung und Verbreitung, Konflikte und Gestaltungsmöglichkeiten, Berlin: Edition Sigma, 1997; Les citoyes appellent à la prudence face aux plantes transgéniq
- (genuine) The original song is a delusional meritocratic anthem for Soulcycle moms, young gays, sigma male grindset hustlers and twitch streaming egirls who think anyone 
- (genuine) H = — [sigma] pi log pi is the entropy of the amount of the probabilities pi… .

### teamsters  [general] 총 17 / genuine 2 (12%)
- 분포: capinit 1, cap 14, genuine 2
- (cap) The news concludes an ongoing dispute between the fair’s organizers and employees that at one point led activists (on behalf of the Teamsters, the New York Dist
- (cap) Calling the outcome of the latest negotiations “a great win,” George Miranda, president of the Teamsters Joint Council 16 and leader of the talks, said: “We’re 
- (genuine) This essay explores Sekula’s emphasis on embodiment as the quality that makesWaiting for Tear Gascapable of describing the otherwise amorphous relation between 
- (genuine) Moving among ‘the teamsters and the turtles’, to use the colloquial description of the makeup of the motley crew that formed the ranks of the anti-WTO (World Tr

### breve  [general] 총 16 / genuine 2 (12%)
- 분포: capinit 2, cap 12, genuine 2
- (cap) He returns once again on Fabio Perletta’s label with Materia Breve, comprising fifteen fleeting compositions (only one is over five minutes long), offering a de
- (cap) Unlike Jisei, who meditated on the Japanese concept of farewell poetry, Materia Breve seems to address the presence, the materiality of sound that, however ephe
- (genuine) Titled Librettos, the series at A+P overlaps Manuel de Falla’s 1904 class-driven opera La vida breve(Life is Short) with a 1967 Stokely Carmichael speech briefi
- (genuine) The fair will feature 18 Mexican galleries, including returning exhibitors like Arredondo \ Arozarena, LABOR, joségarcía ,mx, Lodos gallery, Lulu, Galería Agust

### minder  [general] 총 16 / genuine 2 (12%)
- 분포: cap 10, noneng 4, genuine 2
- (cap) The Worship — Dinner Performance, an original idea from Maya Minder, Hackteria, takes elements of #asrm (autonomous sensory meridian response) as a way to explo
- (cap) COPY PASTE Exhibition Curator: Antonio Roberts Featured artists: Carol Breen (IR), Constant (BE), Lo Vid (US), Lorna Mills (CA), Matthew Plummer-Fernandez + Jul
- (genuine) Das Ars Electronica Center bewohnt nicht minder unseren kollektiven Bewußtskills of watchful preparedness, of standing back in a state of almost Zen-like readin
- (genuine) In her living room, Madame fusses and fights with Merit, her house girl, seeing things, lashing out at her young minder though she thrives by suckling at her ba

### parson  [general] 총 16 / genuine 2 (12%)
- 분포: allcaps 1, capinit 1, cap 12, genuine 2
- (cap) Smerdon, Kurt Submerged and Ted Parson, imprint very particular atmospheres that are both melancholic and fascinating.
- (cap) Farrell and McNamara have designed and built many structures, such as the Parson’s Building for Trinity College, Dublin; the Dunshaughlin Civic Offices in Dunsh
- (genuine) He claimed that the idea for evolution by natural selection occurred to him after reading the famous Essay on Population by Thomas Malthus, a late-eighteenth-ce
- (genuine) He claimed that the idea for evolution by natural selection occurred to him after reading the famous Essay on Population by Thomas Malthus, a late-eighteenth-ce

### rota  [general] 총 16 / genuine 2 (12%)
- 분포: trunc 2, capinit 3, cap 9, genuine 2
- (cap) 53rd INTERNATIONALART EXHIBITION –LA BIENNALE DI VENEZIA 2009Rota Ivancich Palace Castello 4421(close to San Marco square)30122 Venice
- (cap) The pavilion will be located in the historic Rota Ivancich Palace, built in the 16th century, next to Querini Stampalia Foundation, close to San Marco square, i
- (genuine) On Thursday evenings at 6pm, during the extended opening hours of Museion, the following videos by the artist will be shown on the museum’s basement floor on a 
- (genuine) Carsten Nicolai’s “rota”, for example, a giant steel rotating dream machine, was well-made, effectively reflecting the fundamental proportions of Ian Sommervill

### winded  [general] 총 16 / genuine 2 (12%)
- 분포: hyph 14, genuine 2
- (hyph) intoxicating”), and then a long-winded fried-eggs-versus-omelets analogy by MIT Media Lab founder Nicholas Negroponte, Ferguson pounced.
- (hyph) In contrast,Making Art Global (Part 2):‘Magiciens de la Terre’1989is somewhat long-winded, with a turgid introduction by Pablo Lafuente giving way to a narrativ
- (genuine) During August I read that Lauren Berlant, apparently standing in tree pose, replied to a particularly long winded question after a keynote they’d given: There a
- (genuine) No one?”) and the next he is dancing to the Temptations’ “Papa Was a Rolling Stone.”He gets winded and confesses he smokes.

### amours  [general] 총 8 / genuine 1 (12%)
- 분포: cap 6, noneng 1, genuine 1
- (cap) Long in the planning, and sensitively curated by Ambika P3’s Michael Mazière jointly with the filmmaker duo A Nos Amours (Joanna Hogg and Adam Roberts), this su
- (cap) “NOW” follows on from, and in a sense completes, the retrospective of Akerman’s entire filmic output orchestrated by A Nos Amours at the ICA London.
- (genuine) It’s captured in the noble air of “Stratum” and the generative minimalism of “You” and evoked by their revivals of fourteenth- and sixteenth-century composition

### apostle  [general] 총 8 / genuine 1 (12%)
- 분포: cap 5, hyph 1, noneng 1, genuine 1
- (cap) Malcolm Gladwell, corporate consultant, journalist (New York Times) and best-selling author (The Tipping Point) sees the workings of the “Matthew effect” (named
- (cap) It is as if Fisher was challenging anyone to repudiate the Apostle and Christ Himself as religious and ecclesiological authorities.
- (genuine) Call me a cynic (I preferskeptic), but when I heard that Peaches intended to perform, solo, the entirety of Jesus Christ Superstar, with piano accompaniment by 

### bonk  [general] 총 8 / genuine 1 (12%)
- 분포: allcaps 1, cap 6, genuine 1
- (cap) Marcel Duchamp, in a letter to Katherine Dreier dated March 5, 1935, quoted in Ecke Bonk,Marcel Duchamp: The Box in a Valise(New York: Rizzoli, 1989), 147.
- (cap) I rely on Bonk’s book for the description of the Boîte-en-valisethat follows.
- (genuine) Audio analysis includes amplitude, beat detection, bonk, Mel scale, FFT and pitch.

### brigadier  [general] 총 8 / genuine 1 (12%)
- 분포: cap 4, hyph 3, genuine 1
- (cap) The cleverest of the anonymous internet situation room photo edits was a tight crop of the intensely-focused Obama wielding a Playstation controller alongside a
- (cap) (Four out of the six available Warhols failed to sell, reports the New York Times.) Meanwhile Lucian Freud’sThe Brigadier, 2003-2004, fetched $31 million, sligh
- (genuine) ,”La coquillecoheres as a series of potent symbols (cockles, skeleton keys, mirrored orbs, bared breasts) deployed to advance the scenario of an enfeebled pries

### cropper  [general] 총 8 / genuine 1 (12%)
- 분포: cap 5, urlish 2, genuine 1
- (cap) Safra Visiting Professors have contributed immeasurably to the work of the center and the wider scholarly, curatorial, and scientific community in the visual ar
- (cap) Fowler’s most recent film,The Poor Stockinger, the Luddite Cropper and the Deluded Followers of Joanna Southcott, 2012, deals with New Left historian E.
- (genuine) Debts were deducted from the cropper’s share.

### dauphin  [general] 총 8 / genuine 1 (12%)
- 분포: trunc 3, cap 4, genuine 1
- (cap) Gary Dauphin writes and builds websites.
- (cap) Then we decamped to the seaside restaurant Le Dauphin for dinner.
- (genuine) Both friends went on to become filmmakers: Nichols the dauphin of upscale entertainment, Elaine May the dark sorceress of avant-garde screwball comedy.

### hatted  [general] 총 8 / genuine 1 (12%)
- 분포: hyph 7, genuine 1
- (hyph) “But he could also be referring to the end of any relationship, or just a desire not to be trapped.” Whatever Wächtler meant by it, the top-hatted character mak
- (hyph) “What does this represent?” asks a swanky cowboy-hatted viewer pointing the finger at a Cubist painting; the other half we don’t see at Sgomento is the anthropo
- (genuine) She is hatted or unhatted; glimpsed frontal, profile or three quarters; dressed in dark reds, oranges and umber.

### hypo  [general] 총 8 / genuine 1 (12%)
- 분포: trunc 1, capinit 1, cap 5, genuine 1
- (cap) The exhibition is sponsored by:Kulturstiftung des Bundes, Hypo — Kulturstiftung,Bayerisches Staatsministerium für Wirtschaft, Forschung und Kunst
- (cap) The company’s artistic and cultural heritage is mainly derived from the collections of UniCredit in Italy, Hypo Vereinsbank in Germany and Bank Austria.
- (genuine) It has the little camera in it and a couple of rolls of film and MQ developer and hypo in a little tank and so forth.

### juniors  [general] 총 8 / genuine 1 (12%)
- 분포: cap 6, urlish 1, genuine 1
- (cap) Im Sportteil war zu lesen, dass die Argentinos Juniors über Sportivo Alsina mit 4:1 gewonnen hatten, und die Unterhaltungsseiten bewarben einen Technicolor-Schi
- (cap) In sports, Argentinos Juniors beat Sportivo Alsina by 4 goals to 1 in their campaign to reach the premier league, and the entertainment pages promote Pirates of
- (genuine) WORKSHOP: Artificial Intelligence 16 to 18-year-old juniors demonstrate how to develop "intelligent" programs with LOGO.

### lidded  [general] 총 8 / genuine 1 (12%)
- 분포: hyph 7, genuine 1
- (hyph) On top of the ruins of the collage portrait, Picabia painted the outline, heavy-lidded eyes and vampish red lips of afemme fatale, her long-fingered hands drape
- (hyph) Staring down three decades of velocity, Lucas barely blinks, although in the outsized photograph that appears in This Jaguar’s Going to Heaven, her eyes are hal
- (genuine) What questions would you ask of this lidded pot by Karen Karnes?

### lief  [general] 총 8 / genuine 1 (12%)
- 분포: cap 1, noneng 6, genuine 1
- (noneng) Diesem Team oblag auch der Betrieb des ersten Servers, über den im Frühsommer 1995 noch wenig mehr lief als die E-Mails des leitenden Trios Gerfried Stocker, Ju
- (noneng) Am Anfang herrschte ein bisschen Verwirrung und das festival lief gefahr, zwischen popmusik, Messe, ars metallica, ars pneumatica und ars pyromanica, also zwisc
- (genuine) At the heart of Roggenbuck’s work is the injunction to “live [your] lief ” because, of course, YOLO.

### mongoose  [general] 총 8 / genuine 1 (12%)
- 분포: allcaps 1, cap 4, urlish 2, genuine 1
- (cap) LIbrary: System Integration: Ars Electronica Futurelab (AT) Fuwapica & RGBy Interactive stools designed by Japan’s Mongoose Studio invite you to linger a while.
- (cap) Fuwapica & RGBy: Mongoose Studio, Tokyo (JP) http://mongoose.proto-type.jp/products/rgby/ CATS Bilbao combines art and standard medical and industrial engineeri
- (genuine) It is the time of animals somehow immobile in their very movement: the faceless porcupines in their equally blind corner, the mongoose suspended mid-scuttle in 

### nutcracker  [general] 총 8 / genuine 1 (12%)
- 분포: cap 7, genuine 1
- (cap) For instance, since the 1980s they’ve used Tchaikovsky’s Nutcracker March as the de facto soundtrack for meetings of heads of state.
- (cap) Abramović’s fearless embrace of kitsch has fit right into this frame, as in her “living installation”Entering the Other Side, 2005, with its Marian iconography 
- (genuine) The next scene on the same channel abruptly cuts to the dim outline of a whirring machine—likely a palm nutcracker outfitted with a kernel separator.

### retriever  [general] 총 8 / genuine 1 (12%)
- 분포: cap 6, hyph 1, genuine 1
- (cap) This is exactly what Art Retriever aims to prevent.
- (cap) Art Retriever is updated daily with information from several online databases.
- (genuine) Forrest Gump, Kippy’s giant pet retriever, sat caged in the back.

### westerner  [general] 총 8 / genuine 1 (12%)
- 분포: cap 7, genuine 1
- (cap) Bowles’s protagonist is a professor revisiting Morocco, but in Rivers’s take he seems just another clueless Westerner in an alien culture.
- (cap) As the easternmost outpost of Switzerland’s presiding marketplace for contemporary art, Art Basel Hong Kong still provides not just a momentous shopping spree b
- (genuine) On another one a little girl from the Hmong tribe appears, hiding between the thick foliage of a forest that has the appearance of a luscious LSD trip; is she h

### borscht  [general] 총 15 / genuine 2 (13%)
- 분포: cap 11, hyph 1, urlish 1, genuine 2
- (cap) And around a decade ago, some kids in Miami, many of them graduates or current students at the New World School of the Arts, a magnet high school downtown, form
- (cap) I was thinking about this while walking along Biscayne Boulevard toward the Intercontinental Hotel in downtown Miami, whose external LED lights had been program
- (genuine) In the dining room, guests could help themselves to caviar, borscht, stroganoff, and other Russian tasties from buffet tables, and then find their own seats on 
- (genuine) Still in the orange grove with vodka, borscht, and tears, a few lost geese, and the diagonal lines of defeat.

### flatland  [general] 총 15 / genuine 2 (13%)
- 분포: allcaps 1, capinit 1, cap 11, genuine 2
- (cap) Set in a 2-dimensional world inhabited by various polygons, Flatland is a strange mix of philosophy, geometry, and fantasy that punches well above the weight of
- (cap) The works included include: 'Flatland' by Angela Detanico and Rafael Lain, formal abstraction and dynamic views of the Mekong River delta, 'Corpora.proceed (sky
- (genuine) We have extended Virilio's concern to the varied world of the Net, we have lost our bearings in the flatland of data offered by our "regular" browser, and exper
- (genuine) As "spacemakers" [Walser, 1990], we have therefore undertaken the task to "escape flatland" [Tufte, 1990], to design an information browser that organizes infor

### morrow  [general] 총 15 / genuine 2 (13%)
- 분포: capinit 2, cap 10, hyph 1, genuine 2
- (cap) Tony Tulathimutte is the author of Private Citizens(William Morrow Paperbacks, 2016).
- (cap) But Wintergarden’s aim is to avoid a nostalgic visual style, and it does this using Morrow’s dayglo costumes, assembled from high-tech fabrics and influenced by
- (genuine) The party spilled into the morrow, when Cardiff Contemporary, a citywide visual-arts festival, had its opening night.
- (genuine) Further revelry followed on the morrow, when dealers Francesca Galloway and Amrita Jhaveri benevolently hosted a Summer Party.

### rooks  [general] 총 15 / genuine 2 (13%)
- 분포: cap 13, genuine 2
- (cap) Lawrence Shainberg’s long profile of Conrad Rooks at the 1966 Venice Film Festival, where he had arrived to show his psychedelic vanity picture Chappaqua, is a 
- (cap) Jurors for the 2014 awards included Michael Rooks, curator of the High Museum, Carter Foster, curator of drawings at the Whitney Museum of American Art, and Chr
- (genuine) There are grounds for the assumption that the great chess rules reform in the early modern age greatly increased freedom of movement for officers like bishops a
- (genuine) There are grounds for the assumption that the g reat chess rules reform in the early modern age greatly increased freedom of movement for officers l i ke bishop

### trilling  [general] 총 15 / genuine 2 (13%)
- 분포: cap 12, noneng 1, genuine 2
- (cap) Writing in the wake of World War II, the literary critic Lionel Trilling argued for the continued importance of manners as the very basis of what he called “mor
- (cap) the nature of the very food we prefer.” Trilling’s seminal essay “Manners, Morals, and the Novel” was published in his 1950 book The Liberal Imagination, which 
- (genuine) One is reminded of Madame Arpel’s trilling injunction in Jacques Tati’sMon oncle(My Uncle, 1958), “You must get used to these things!
- (genuine) The initial plaintive trilling gave way to a charging, moneyed insistence familiar to anyone on the global art circuit.

### aft  [general] 총 14 / genuine 2 (14%)
- 분포: allcaps 2, capinit 1, cap 7, hyph 1, urlish 1, genuine 2
- (cap) 1'0 Ultunl SP'tAI(I."� "Nt lt �"l.tH$'1'tlN lti8(;f tUC1"HCU\.Aft $MUH.
- (cap) The Drums of the Fore and Aft
- (genuine) Four castors—two fore, two aft—have been built in for stabilization purposes.
- (genuine) water in the estuary, the shower nose held above and belowbefore and aft (for no man, a sparmate, appreciates the sick – any more than his wife will)yellow wing

### anon  [general] 총 14 / genuine 2 (14%)
- 분포: allcaps 1, cap 7, hyph 3, urlish 1, genuine 2
- (cap) If you want it!”– Anon, 2018
- (cap) The linchpin of the work is his title's invocation of Ad Herennium (Anon., ca.
- (genuine) That is, Bachelard fails to confront the actuality of the dream-state, which per Kelley (and more anon) was far from an ideal calm.
- (genuine) See also Work, Made-ready, Kunsthalle Bern and Homemade twenty pence piece (anon)… .

### auger  [general] 총 14 / genuine 2 (14%)
- 분포: allcaps 1, cap 10, hyph 1, genuine 2
- (cap) This prototype can not transmit in turn signals, and was designed by two graduates of the Royal College of Art: James Auger and Jimmy Loizeau.
- (cap) This prototype can not transmit in turn signals, and was designed by two graduates of the Royal College of Art: James Auger and Jimmy Loizeau.
- (genuine) However, the apparent incompatibility of the third couple, Joshua Butterby and Minerva Crane, does not auger well for future harmony.
- (genuine) Yes, we see a cast of a behind, and a partial mask with a pipe going through the mouth, and an auger as a potential penetrator, and most of the round pieces in 

### cramps  [general] 총 14 / genuine 2 (14%)
- 분포: capinit 2, cap 9, urlish 1, genuine 2
- (cap) LP – Dialogo | Cramps Records
- (cap) LP – Dialogo | Cramps Records
- (genuine) (Luc had earlier described Rosetta’s abdominal cramps as “birthing pains that deliver no child.”) More classically shot than the Dardennes’ previous quartet,Lor
- (genuine) And the idea of home is at the center of Costa’s film: the home you want and the one you settle for, how the one you settle for defines and then cramps the boun

### errata  [general] 총 14 / genuine 2 (14%)
- 분포: capinit 1, cap 10, urlish 1, genuine 2
- (cap) Guest curator for Futurefarmers: Errata—Brief Interruptions:Rebecca Uchill
- (cap) A Conceptual art–like listing of the set appeared in the artist’s booksLast Night, 2013, and Last Night: Errata, vols.
- (genuine) Lynn Hershman Leeson, Jo Hanson, and Pat Tavernier, (H)errata, 1977, The Floating Museum.
- (genuine) They write their apologies and add them in like inserts – an errata sheet, you know?

### gazelle  [general] 총 14 / genuine 2 (14%)
- 분포: cap 8, hyph 3, urlish 1, genuine 2
- (cap) Included are samples from specific locations and time, as well as tracks featuring musicians elaborating on these field recordings (Loscil, Matmos, The Field an
- (cap) Included are samples from specific locations and time, as well as tracks featuring musicians elaborating on these field recordings (Loscil, Matmos, The Field an
- (genuine) She was obsessed with a small gazelle figurine from ancient Egypt that she found at the Met.
- (genuine) The gazelle, for example, looks strikingly like Bambi, and I feel pretty sure that she made that connection.

### lope  [general] 총 14 / genuine 2 (14%)
- 분포: trunc 3, capinit 1, cap 8, genuine 2
- (cap) This series is inspired in part by the play El Acero de Madrid (The Steel of Madrid) , written by Lope de Vega in 1608.
- (cap) The innocent, timid, orphaned teenager becomes the ward of Don Lope (Buñuel regular Fernando Rey), a lecherous, hypocritical, overweening Manchegan aristocrat w
- (genuine) They lope up a spiral ramp and get into position.
- (genuine) They lope up a spiral ramp and get into position.

### mariner  [general] 총 14 / genuine 2 (14%)
- 분포: capinit 1, cap 10, hyph 1, genuine 2
- (cap) Driven by artists such as Molly Crabapple, Sarah Ray, and the Fang Collective, the campaign claims that Mariner is “profiting off of human misery”and must be re
- (cap) June Kramer, a member of Fang Collective, told Hyperallergicthat “the Kemper Museum has five people on their board of trustees who either currently or recently 
- (genuine) Framed though it is in the traditional language of sin and redemption, it can also be read as a story of the mariner’s mental breakdown after an overwhelming cr
- (genuine) The mariner then sold the work, which dates to 300 to 100 BCE, and the museum eventually purchased it for $3.95 million from a German dealer in 1977.

### austral  [general] 총 13 / genuine 2 (15%)
- 분포: cap 11, genuine 2
- (cap) Galeriá Réplica, Institute of Visual Arts Faculty of Architecture and Arts, Universidad Austral de Chile (CL) Extractivisms: Operations and Practices produced b
- (cap) Lañilawal remains in the mode of a deferred time, literally a mysterious interval removed from the time scale of human Universidad Austral de Chile (CL) LAÑILAW
- (genuine) Throughout the long 2011 austral winter, Chilean students took over the streets to stand against the overall privatisation of the education system (established 
- (genuine) It is possible to practise speleology in contemporary figurative art, using music as an evocative, subjective austral metaphor.

### burghers  [general] 총 13 / genuine 2 (15%)
- 분포: cap 10, urlish 1, genuine 2
- (cap) PLATEAU, Samsung Museum of Artwas first inaugurated in 1999 as Rodin Gallery, presenting its permanent installation of Auguste Rodin’s monumental masterpieces T
- (cap) PLATEAU, Samsung Museum of Art was first inaugurated in 1999 as Rodin Gallery, presenting its permanent installation of Auguste Rodin’s monumental masterpieces 
- (genuine) Uncritical consumers, unassertive burghers and traditional workers are increasingly becoming anachronistic, obsolete models ready to be consigned to the junk he
- (genuine) Uncritical consumers, unassertive burghers and traditional workers are increasingly becoming anachronistic, obsolete models ready to be consigned to the junk he

### cedars  [general] 총 13 / genuine 2 (15%)
- 분포: cap 11, genuine 2
- (cap) Boyle, who collaborated with Alfred Hitchcock and Norman Jewison, and was the recipient of an honorary Oscar in 2008, died Sunday of natural causes following a 
- (cap) Currently, Berg is on the boards of the American Friends of the Israel Museum, the Zimmer Children’s Museum, Today’s and Tomorrow’s Children Fund at UCLA, and t
- (genuine) We would also take trips to places with landscaped gardens, such as Burton Constable, Newby Hall and Castle Howard, where we could see huge, towering cedars and
- (genuine) The ones with me also think it’s beautiful and the cedars are so close.

### clit  [general] 총 13 / genuine 2 (15%)
- 분포: capinit 1, cap 8, hyph 1, urlish 1, genuine 2
- (cap) I ran the Clit Club, which was cofounded in 1990 by myself and Jaguar Mary.
- (cap) In this important moment, the Clit Club and the Pork parties overlapped on the West Side but both parties also moved around to different spaces too.
- (genuine) Granted this is wordplay, but it is towards underscoring the way in which female parts, be they part of the domesticated and industrially siphoned animal (udder
- (genuine) “I HOPE NO ONEgets a clit cut off in this movie,” a colleague sitting next to me said this morning before Lars von Trier’s Competition entry Melancholia.

### dukes  [general] 총 13 / genuine 2 (15%)
- 분포: cap 11, genuine 2
- (cap) There is a text, dated between 1572 and 1574, in which the literate Ludovico Agostini describes a day in August that he spent at Villa Imperiale, court of the D
- (cap) It was never completed due to the sudden death of Francesco Maria della Rovere, and therefore never fully experienced as the original intentions of the Dukes.
- (genuine) One small consequence of the Trump victory is that a sense of social mission, however misplaced, has become de rigueur for the dukes and duchesses of the cultur
- (genuine) The underlying story is that part of the museum’s collection consists of spoils, trophies, and diplomatic gifts that ended up in the hands of the Burgundian duk

### sombrero  [general] 총 13 / genuine 2 (15%)
- 분포: cap 6, hyph 1, urlish 2, noneng 2, genuine 2
- (cap) © Tom Mesic © Sombrero Design
- (cap) Jill MagidWoman With Sombrero November 2–December 21, 2013
- (genuine) He’s positively mellow in The Wonderful Country(1959), in which his oversize sombrero reflects his general discomfort fending off the law on one side of the Mex
- (genuine) In his choice of hat he alternated between a Stetson and a sombrero, teetered on stage in a pair of red high heels and brandished a toy gun before the audience.

### untie  [general] 총 13 / genuine 2 (15%)
- 분포: cap 11, genuine 2
- (cap) Resonances is a space for research and encounter accompanying each exhibition of the Untie to Tieprogramme.
- (cap) Corresponding with each respective chapter of Movement.Bewegung, the platform brings together voices, thoughts and words, connecting and collaborating with init
- (genuine) Divorce became a veritable industry in Reno, where dude ranches catered specifically to those looking to untie the knot.
- (genuine) Within these nodes, information is accumu lated, processed, and trans­ m itted, but the nodes themselves are not anything: if we undo them (untie the relational

### viper  [general] 총 13 / genuine 2 (15%)
- 분포: allcaps 1, capinit 1, cap 9, genuine 2
- (cap) Colossal Youthwas released in 2006, by which time digital had begun to make significant inroads in Hollywood productions—take Michael Mann’sMiami Vice, shot wit
- (cap) The same company is in the icono-sound installation The Hall of the Viper and the Giant Worms , as vertiginous as a pit plunging from heights to depths of the a
- (genuine) The family crest, a crown-bedecked zigzag of a viper swallowing a man usually described as a Moor, can be found everywhere in the city, and you’ve probably seen
- (genuine) Pretty girl, the heavens rest in the coiled viper; this you know I know.

### apricots  [general] 총 12 / genuine 2 (17%)
- 분포: capinit 2, cap 8, genuine 2
- (cap) In third place:Apricots from Damascus, to be presented in Istanbul, Turkeysubmitted by: Atif Akin & Dilek Winchester Apricots from Damascusinvites artists to pr
- (cap) In third place:Apricots from Damascus, to be presented in Istanbul, Turkeysubmitted by: Atif Akin & Dilek Winchester Apricots from Damascusinvites artists to pr
- (genuine) He also prints a zine on apricots, which he sees as an ideal model for migration flows.
- (genuine) In July I taught poetry in Tbilisi, a shimmering blonde city full of wine, casinos, flushed apricots, and handsome people with dark hair and red lips and high c

### chemo  [general] 총 12 / genuine 2 (17%)
- 분포: cap 4, hyph 6, genuine 2
- (hyph) As a chemo-physicist and early theoretician of electricity, he accepted only different states of oscillation of material entities that are very much alive.
- (hyph) Donald had used the chemo-related hair loss as an opportunity to get a Trilby, a Bowler, a Homburg, and something called a Rush Street, which is what I ordered 
- (genuine) “My insurance doesn’t cover chemo, so if this lump I feel is cancer I’m fucked” isfear.
- (genuine) “Lives of Performers” punctuated his chemo treatments and his days about in London: at the National Gallery with Gainsborough, films with Mike and Rachel, piano

### depositions  [general] 총 12 / genuine 2 (17%)
- 분포: capinit 1, cap 9, genuine 2
- (cap) Suspended Depositions is a novel rapid prototyping approach that aims to blur the line between processes of design and fabrication.
- (cap) Suspended Depositions takes a very different approach, by injecting a continuous stream of UV-curable liquid resin into a viscous gel.
- (genuine) Levine is also seeking a court order that John and Kristine Woodward each provide depositions on the purchases.
- (genuine) Although he had been given at birth another name, “Dahham,” he refused to respond to it, with the result that eventually his family yielded and called him “Cemi

### godson  [general] 총 12 / genuine 2 (17%)
- 분포: cap 9, urlish 1, genuine 2
- (cap) Edited by Tessa Giblin Texts by Silvia Federici, Tessa Giblin, Lisa Godson, and Tina Kinsella Buy on moussepublishing.com
- (cap) Jürgen Scheible Lenin’s Godson’s Mobile ArtBlog The Mobile ArtBlog is a blog of digital art images created with a mobile phone.
- (genuine) (His godson, too, appears in these ruins, awaiting a paycheck more than twenty years overdue.) Occasional exterior shots, including one of a forest at night, on
- (genuine) I was in my godson’s photography studio when Slow Productivityby Cal Newport fell out of his tote bag by mistake.

### hubby  [general] 총 12 / genuine 2 (17%)
- 분포: capinit 2, cap 8, genuine 2
- (cap) Film was just one of many mediums for Tony Conrad, whose limitless capacity for invention is ably captured in Tyler Hubby’sTony Conrad: Completely in the Presen
- (cap) Screening: Tony Conrad Films In conjunction with Introducing Tony Conrad: A Retrospective Friday, October 19, 7 and 9pm7 pm: Conrad's classic 16mm films, includ
- (genuine) “I’m surprised to see my own work here,” said Glenn Ligon, browsing with Studio Museum director Thelma Golden and her British hubby, designer Duro Olowu.
- (genuine) And there were the stalwarts: art historian Geeta Kapur with her hubby, artist Vivan Sundaram; Bombay-born cultural theorist Homi Bhabha.

### lager  [general] 총 12 / genuine 2 (17%)
- 분포: trunc 1, cap 5, urlish 3, noneng 1, genuine 2
- (cap) Unterschied Kandinsky noch das "große Reale" vom "großen Abstrakten", das er etabliert hat, und ist die Kunst in der Folge in diese beiden Lager gespalten, so l
- (cap) Torbjørn Rødland, Golden Lager , 2006 Torbjørn Rødland, Shuttlecocks , 2011 Tabor Robak, Vatican Vibes , 2011 Adriana Lara, Laser Painting , 2012 Darren Bader, 
- (genuine) Before the screaming and the bourbon and the nudity and the lager, though, there was a panel.
- (genuine) The last has already been achieved at the Schaulager in Münchenstein/Basel, conceived by Maja Oeri as a storehouse (lager) where works belonging to the Emanuel 

### walling  [general] 총 12 / genuine 2 (17%)
- 분포: cap 10, genuine 2
- (cap) This book of essays, written by the artist Mary Walling Blackburn between the 2010s and the present, moves with near-psychedelic precision across American time 
- (cap) "No one thinks to the brink quite like Mary Walling Blackburn.
- (genuine) The museum is walling off the exhibit, which features works that have been described as“racially and sexually charged,”so that it can first explain the exhibit 
- (genuine) And this becomes possible because the construction of the FESTAC Village is not completed at the time of the festival, without the kind of fencing or walling th

### yelp  [general] 총 12 / genuine 2 (17%)
- 분포: cap 10, genuine 2
- (cap) Droitcour’s perspective is unique: His Yelp reviews of arts institutions exist alongside his contributions to Art in America, where he is an editor.
- (cap) “That’s Yelp now,” Willsdon mused.
- (genuine) It’s strange to see them written out, twitching nakedly on the page—severed from his yelp, his bile, his screech, his sneer, his glamorous dysfunction and ratty
- (genuine) Here, after rapping about being left, then about how relieved he was to be left, he lets out a scratchy yelp—part anguished scream, part sinister cackle, part e

### bade  [general] 총 11 / genuine 2 (18%)
- 분포: cap 9, genuine 2
- (cap) As with my previous “staged” video projects, which are sometimes shot on site, at the actual places that the film refers to—as with Factory, 2003,Bade Area, 200
- (cap) Alexander and Bonin Gallery has announced that it will be moving to 47 Walker Street in Tri Be Ca this summer, occupying two floors and over 7,000 square feet o
- (genuine) From there the mosque’s call to prayer bade us to a nearby 1970s bunker, called Bunk’Art 2, adjacent to one of many government buildings constructed by the Ital
- (genuine) A stranger lobbed a straw cowboy hat at me in the sun and bade me keep it.

### bunt  [general] 총 11 / genuine 2 (18%)
- 분포: cap 6, urlish 1, noneng 2, genuine 2
- (cap) Stuart Bunt, Ionat Zurr, Oron Catts, Gil Weinberg, Matt Richards, Iain Sweetman) Stuart Bunt/AUS, Natalie Jeremijenko/USA Hiroaki Kitano/J, Joe Davies/USA Moder
- (cap) Stuart Bunt, Ionat Zurr, Oron Catts, Gil Weinberg, Matt Richards, Iain Sweetman) Stuart Bunt/AUS, Natalie Jeremijenko/USA Hiroaki Kitano/J, Joe Davies/USA Moder
- (genuine) They are much less susceptible than earlier cameras to the image "bunt" that can permanently damage the tubes.
- (genuine) The workshop gradually acquired and bunt equipment, and the members had time to leam the medium in a crafts­ manlike fashion.

### coitus  [general] 총 11 / genuine 2 (18%)
- 분포: capinit 1, cap 1, hyph 4, urlish 3, genuine 2
- (hyph) Mid-coitus—and while on the lam from Curly’s rifle-toting father, with helicopters and hounds on their trail—Armand can’t resist telling his adolescent lover th
- (hyph) I settled back into positions sometime after midnight and stayed until nearly 2 AM, watching men in bed look nervously at digital alarms, couples post-coitus, p
- (genuine) He frequently included stylized vaginal forms that he called Vögeln (Swiss German for “little birds,” slang for coitus).
- (genuine) Has Koons ever made a sculpture that didn’t suggest hetero coitus?

### forevermore  [general] 총 11 / genuine 2 (18%)
- 분포: cap 7, urlish 2, genuine 2
- (cap) Marnie Weber “Once Upon a Time in Forevermore” “Once Upon a Time in Forevermore”, Marnie Weber’s exhibition gathers together a series of collages as well as a d
- (cap) Marnie Weber “Once Upon a Time in Forevermore” “Once Upon a Time in Forevermore”, Marnie Weber’s exhibition gathers together a series of collages as well as a d
- (genuine) And of those who hardly remember an iota but appeared on the programs of various Happenings or hobnobbed over cocktails, etc., with Sturtevant, there was even a
- (genuine) Grandma Perry then tells her granddaughter that she can’t wait to hear the results and that, furthermore, forevermore, she loves her more.

### huntsman  [general] 총 11 / genuine 2 (18%)
- 분포: capinit 1, cap 8, genuine 2
- (cap) I love him, I love him, I’m so sorry.” joségarcia, mx and Attilia Fattori Franchini are proud to present “Snow White and the Huntsman”, an exhibition of new wor
- (cap) The show takes its title from the 2012 motion picture starring Kristen Stewart as Snow White and Chris Hemsworth as the Huntsman; a movie which was met with lit
- (genuine) One vividly depicts the thirty-six fruits now extinct due to illegal logging in Sabah (a Malaysian state in northern Borneo); others show weasel-like animals la
- (genuine) The Ellipse, depicting a huntsman whose rifle appears where his nose should be, The Old Soldier (a poor, ill, veteran who can no longer fight, decked out with f

### hypocrite  [general] 총 11 / genuine 2 (18%)
- 분포: allcaps 1, cap 6, urlish 2, genuine 2
- (cap) 6 manuel arturo abreu, “Is Theorizing Cannibalism Ethical?,” Hypocrite Reader, no.
- (cap) Scourti is an AHRC-funded PhD student at Goldsmiths, and is guest editor of the Happy Hypocrite journal (forthcoming 2019).
- (genuine) To start listening to them again would be the first step towards a coming common language, which is not rooted in the hypocrite presumption of a unity of humank
- (genuine) People thought Morris’s involvement in politics was ridiculous, and that he was a hypocrite – a rich person being a socialist.

### loin  [general] 총 11 / genuine 2 (18%)
- 분포: capinit 1, cap 6, urlish 1, noneng 1, genuine 2
- (cap) The composer whose opera L’Amour de Loin would delight audiences at the salzburg Festival years later looked to be in at least her ninth month of pregnancy when
- (cap) oder das Zusammentrefen mit der komponistin kaja Saariaho, die hochschwanger die goldene Nica in empfang nimmt und Jahre später mit ihrer oper L’ Amour de Loin 
- (genuine) By a skilled sleight-of-hand, hams, shoulders, clear, mess, and prime fly off, each squarely cut to its own place, where attendants aided by trucks and dumb-wai
- (genuine) Bush, a black square, a loin of pork, some quantum mechanics and so on).

### lop  [general] 총 11 / genuine 2 (18%)
- 분포: trunc 5, capinit 1, cap 1, hyph 2, genuine 2
- (trunc) With the support of: Théâtre de lOpéra – Rome, Teatr Wielki – Warsaw, Polish Institute – Paris, Polish Institute – Rome, Staats Oper Unter den Linden – Berlin, 
- (trunc) With the support of: Théâtre de lOpéra – Rome, Teatr Wielki – Warsaw, Polish Institute – Paris, Polish Institute – Rome, Staats Oper Unter den Linden – Berlin, 
- (genuine) Cursed are we who lop the tops off trees to find heat’s
- (genuine) So, for example, if the artist found that in one of his pictures the corner of a pool table had been cut off by the Polaroid’s white border, he would actually l

### puss  [general] 총 11 / genuine 2 (18%)
- 분포: cap 6, hyph 3, genuine 2
- (cap) We made it to the cavernous (and nearly empty) MACRO just in time to see Dash Snow’s film Sisyphus, Sissy Fuss, Silly Puss.
- (cap) Currently based in Copenhagen, Larsen has penned essays on Öyvind Fahlström, Palle Nielsen, and the artists involved in the publication Puss.
- (genuine) “The Golden Kitty award, chosen by visitors to the Walker’s Web site, went to Will Braden for his two-minute opus ‘Henri 2: Paw de Deux,’ about the existential 
- (genuine) A double-head shot of the pair in Harper’s Bazaarconfronts us with Karl’s sunglass-hidden gaze, his white coif tastefully styled into cat ears as he hoists the 

### quorum  [general] 총 11 / genuine 2 (18%)
- 분포: capinit 2, cap 6, noneng 1, genuine 2
- (cap) ars electronica center Kommunikation, das Quorum Sensing, zu gewinnen.
- (cap) Die Kritik der nication, of Quorum Sensing.
- (genuine) Lihn managed to recruit a heterogeneous quorum of left-wing intellectuals, actors, politicians, writers, artists and socialites for the happening-homage-burial 
- (genuine) Relations as defined in the tables of Correspondence by Athanasius Kircher ("Poligraphica seu artificium linguarium, quorum omnibus totis mundi populis poterit 

### revolvers  [general] 총 11 / genuine 2 (18%)
- 분포: cap 9, genuine 2
- (cap) Soft Revolvers · Myriam Bleau The visual aesthetic of this project truly captures the spectacle of light and movement.
- (cap) ISBN 978-3-7757-4022-7 Printed in Austria Cover illustration: Front: Alex Verhaest: Temps Mort / Idle Times; Agnes Meyer-Brandis: Teacup Tools Back: Nobumichi A
- (genuine) The artist often jokes in letters about thecanon bibital(private “gun”), and around this time addressed a postcard to “Monsieur ELT Mesens (manufacturer of mars
- (genuine) In this context, the bringing together of revolvers and madrier planks from the MAH’s arms and armoury collection with the artist’s famous tyres creates a symbo

### sequoia  [general] 총 11 / genuine 2 (18%)
- 분포: cap 8, urlish 1, genuine 2
- (cap) Central to the exhibition are a series of sculptural works carved in 2023, the mother of which was a single ancient Sequoia tree that fell near the artist’s hom
- (cap) Francesca , the tallest of the three siblings in the central room, reaches over three metres in height and is carved from a single piece of wood, taking the for
- (genuine) The earliest tree in Farocki’s history appears in Mystery House(1980): a giant sequoia, depicted as a jagged outline.
- (genuine) Ascending through a chimney up into the canopy of sequoia, and into a cosmic sky to meet singing spirits, Cynthia discovers how to stage a sacrifice to the eart

### batty  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) Mark Batty Publisher, ISBN 978-0979966668, USA, 2009, English
- (cap) “Roy Batty is a good therapist for Rick Deckard in Blade Runner,” quips McGowan – but 1982’s form of (fictional) AI is not a contemporary LLM.
- (genuine) Indeed, it was this feature of Kubrick’s persona that drove so many people batty but that seems to have inspired in Vitali such fierce devotion, a determination
- (genuine) Hyde tale from Frears and screenwriter Christopher Hampton,Mary Reillyis a batty extension of their previous Dangerous Liaisonsinto the overlapping terrain of V

### blizzards  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) As part of its ongoing partnership with Art Basel Paris as Public Program Official Partner, Miu Miu announces “30 Blizzards.”, a major work conceived by artist 
- (cap) “30 Blizzards.” explores a cross-section of different disciplines, the interrelationship between distinct and divergent mediums when placed in proximate dialogu
- (genuine) Using their bodies children can conjure a storm, release a twisting tornado or rain down bolts of lightning from their fingertips.There are mighty wind fields t
- (genuine) The awe of summer thunderstorms, smothering blizzards and window rattling nor’easters left a lasting impression on me.

### chihuahua  [general] 총 10 / genuine 2 (20%)
- 분포: capinit 1, cap 7, genuine 2
- (cap) Gavaldón was himself born in Chihuahua in 1909, the son of a middle-class family with rural roots.
- (cap) Her son Pablo Weisz Carrington sold her home on Chihuahua Street in the city’s Roma neighborhood to UAM for $500,000 in 2017, on the condition that it be turned
- (genuine) So might a chihuahua fix its tiny fangs in the ankle of a bull elephant.¹⁵
- (genuine) After passing a man operating a drone seated with his back to the famed Roosevelt pool, I happened upon Fabio, a tiny white longhair chihuahua sprawled out in N

### coon  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) Modern Luminary By Caroline Coon, Louis Fratino, Nick Goss, Mohammed Z.
- (cap) Caroline Coon is an artist, writer, political activist and a trailblazer of London’s counterculture.
- (genuine) VAGINAL The cut-up Daisy Dukes that went from coon to caint, that was the de rigueur outfit.
- (genuine) I’m a hustlin’ coon, that’s just what I am.

### dings  [general] 총 10 / genuine 2 (20%)
- 분포: trunc 5, urlish 1, noneng 2, genuine 2
- (trunc) Freeman, H., (Hrg): TUTORIAL : SELECTED REA­ DINGS IN INTERACTIVE COMPUTER GRAPHICS, IEEE Computer Society Press, L.A., 1984.
- (trunc) COMPUTER ANIMATION, Procee­ dings of the Second Annual Conference on Computer Graphics and Interactive Techniques-SIGGRAPH, 1975.
- (genuine) Yet Ford’s panels are lifted from her own custom dance floors and bear traces of that former use— sociability, proximity, and connection that lingers in the nic
- (genuine) Dozens of apps needed to be powered up each morning, but Baerenwiese had grown so adept at the task that he could scroll through and update, with likes and ding

### dropper  [general] 총 10 / genuine 2 (20%)
- 분포: cap 2, hyph 2, urlish 4, genuine 2
- (urlish) Homemade calendula and wild pansy syrups represent the artist’s heart, and they are shared with visitors using a dropper.
- (urlish) Homemade calendula and wild pansy syrups represent my heart, and they are shared with visitors using a dropper.
- (genuine) Held up by three chain-linked ropes, a large dropper is suspended over a round black carpet.
- (genuine) The dropper, made of hand-blown glass and resembling one half of an hourglass, is full of slowly seeping, viscous black liquid that could be mistaken for tar or

### flagstaff  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) 1983, Flagstaff, California),Samara Scott(b.
- (cap) I went and joined my Epstein Truther meetup on the steps of the Independence Flagstaff.
- (genuine) In a light breeze, high on the flagstaff of the parade grounds at Fort Laramie, as Fort Williams was later named, the Stars and Stripes were flapping gently in 
- (genuine) Sound artist Jacob Kirkegaard will present Bandera, composed from audio recordings of the flagstaff masts from the United States Interests building in Havana.

### granary  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) Deuchar also oversaw the reorganization of the Art Fund’s staff, structure, and offices—which moved to its new headquarters in Granary Square in 2014—and the es
- (cap) In 2013 the Festival will explore the area adjacent to the Main Town, between Zielona Brama (Green Gate) and Brama Żuławska (Zulawska Gate): Wyspa Spichrzów (Gr
- (genuine) ‘O for the help of Angels to complete this Temple’, wrote Wordsworth after a visit in 1820.37Requisitioned as a granary, ammunition dump, prison and quarry, and
- (genuine) But CUAC has invested heavily in Ephraim, raising money to renovate their building, a granary built by Mormon settlers in the mid-nineteenth century, as well as

### lubrication  [general] 총 10 / genuine 2 (20%)
- 분포: cap 5, urlish 3, genuine 2
- (cap) The History of Lubrication .
- (cap) In The History of Lubrication, Pericàs reflects on how we associate saliva with our bodily intimacy, yet only truly recognize it once beyond the mouth’s thresho
- (genuine) Perhaps the snails are doing just this very thing for us here, that is, providing a thin film of lubrication to aid in our navigation and consumption of the art
- (genuine) Surprising how a little lubrication goes a long way.

### meow  [general] 총 10 / genuine 2 (20%)
- 분포: allcaps 2, cap 4, urlish 1, noneng 1, genuine 2
- (cap) 9THE MEOW, LOS ANGELESThe Meow is a shed in the backyard of the Los Angeles home belonging to artists Lisa Anne Auerbach and Joel Kyack.
- (cap) Over the past year and a half, Auerbach and Kyack have invited independent, artist-run businesses, including a tattoo parlor and a psychic, to temporarily set u
- (genuine) There is a wall made of Cat bricks that meow when you stroke them.
- (genuine) There is a wall made of Cat bricks that meow when you stroke them.

### romaine  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) (I just finished reading the Modigliani bio and realized the author wrote a bio of Romaine Brooks .
- (cap) Anyway it was Lee Krasner, Romaine Brooks, Natalie Barney, Djuna Barnes, Mercedes Matter, Patsy Southgate, Elaine de Kooning, and Ruth Kligman .
- (genuine) [5] “What the hill shape meant to me I am not sure, it is just that paintings of mine based on this shape seemed to be more ‘mine’ than any.” Quoted in Éric de 
- (genuine) The romaine, cut crosswise, had space to stretch its legs.

### shanks  [general] 총 10 / genuine 2 (20%)
- 분포: capinit 1, cap 7, genuine 2
- (cap) By contrast, the largest unaided manual computation of 4 was 707 digits by William Shanks in 1873.
- (cap) By con­ trast, the largest unaided manual computation of 4 was 707 digits by Wi l l iam Shanks in 1 873.
- (genuine) (It’s their destiny as well as their duty, after all.) We watch as Zothe shanks Loth in the kidneys with a screw, forces him to drink expired Drano, cuts off hi
- (genuine) It is a haunting, almost marginal, sketch that depicts the ‘shrunk shanks’, wispy hair and bald pate of the archetypal old man.

### sledge  [general] 총 10 / genuine 2 (20%)
- 분포: cap 7, hyph 1, genuine 2
- (cap) The director’s Napster aesthetic would later lead him to deploy Verdi and Elvis, Wagner and Percy Sledge, Saint-Saëns and the Andrew Sisters, segueing recklessl
- (cap) The sound track shuffles from Fleetwood Mac’s “Sara”to Mario’s “Let Me Love You” to Sister Sledge’s “He’s the Greatest Dancer,” segueing in accordance with the 
- (genuine) It is then destroyed with a sledge hammer.
- (genuine) Having insufficient funds, they rob a Chicken Shack with squirt guns and a sledge hammer.

### squires  [general] 총 10 / genuine 2 (20%)
- 분포: cap 8, genuine 2
- (cap) Nick Squires reports in the Telegraphthat a trove of Roman and Etruscan antiquities that was previously owned by British art dealer, Robin Symes—who was sent to
- (cap) Nick Squires reports in The Telegraphthat Italian art historians claim to have found one hundred works by Caravaggio.
- (genuine) And there they were, a whole sleeping court: knights and barons and squires, ladies-in-waiting, bishops and soldiers, poets and wits.
- (genuine) These tournaments, with their triumphal entries of knights attended by squires, pages and liveried servants, followed a pattern that was popular throughout Euro

### toilette  [general] 총 10 / genuine 2 (20%)
- 분포: capinit 1, cap 7, genuine 2
- (cap) The exhibition will be showcasing such key works as La Toilette de Cathy (1933), Le Roi des Chats (1935), Les Enfants Blanchard (1937), La Patience (1946–8), La
- (cap) The single female figure is a reference to Pierre Puvis de Chavannes work, La Toilette (1883), and acts as a continued depiction of women doing makeup or brushi
- (genuine) Throughout the former, we see Richie’s hand as it investigates the personal objects in his parents’ darkened bedroom, caressing his mother’s toilette articles, 
- (genuine) The women (played by the same actor) do their toilette, communicate in their respective historical modes (hand-writing and telephone), and look contemplatively 

### yon  [general] 총 10 / genuine 2 (20%)
- 분포: cap 4, hyph 1, urlish 3, genuine 2
- (cap) The scenes will include a re-orchestrated interpretation of Stephin Merritt’s pop song The Book of Lovewith vocalist Colin Killalea and a string quartet made up
- (cap) The first part of the exhibition Flooring Horizonswas presented at the Musée de la Roche-sur-Yon from December 13, 2014 to February 21, 2015.
- (genuine) SINCE THE ART WORLDis never in one place very long, membership often means flying hither and yon without knowing what’s in store.
- (genuine) Wilcox, Louise Lawler), curators from hither and yon (Ann Temkin, Joachim Pissaro), the occasional media celebrity (Arianna Huffington, Tina Brown), and the dir

### andante  [general] 총 9 / genuine 2 (22%)
- 분포: capinit 1, cap 6, genuine 2
- (cap) In the article ‘Andante Politics’, published in 2011,
- (cap) For example, in his Krapp’s Last Tape (1958), an elderly man listens to a recording of his own voice; this listening forms the starting point for Moro’s new art
- (genuine) Contemplatively, andante, the pianist strikes a few keys and then draws his hands back again.
- (genuine) Like the gestures of a conductor, the layout, head turned to the left, then to the right,largo,legato,staccato,andante, executes the notes and cadences for whic

### antes  [general] 총 9 / genuine 2 (22%)
- 분포: cap 4, urlish 1, noneng 2, genuine 2
- (cap) Its recipients have included Georg Kolbe (1905), Max Beckmann (1906), Käthe Kollwitz (1906), Ernst Barlach (1908), Gerhard Marcks (1928), Horst Antes (1962), Ma
- (cap) Histories of colonial theft, and the loss and subsequent reanimation of cultural legacies, are similarly the subject of Clarissa Tossin’sMojo’q che b’ixan ri ix
- (genuine) The lead picture on Prince’s page on the Gagosian Gallery site antes up a dirty look: Sporting a collared, keyhole-neckline shirt that laces up crisscross, a sc
- (genuine) Ya nada es como antes Featured artists:Kevin Ávila, Bad Bunny, Liz Cohen, David Cordero, Luis Gispert, Luis Manuel Otero Alcántara, and Joiri MinayaCurated by A

### cantaloupe  [general] 총 9 / genuine 2 (22%)
- 분포: capinit 2, cap 5, genuine 2
- (cap) In 2005, Cantaloupe Music released 1-Bit Music, custom-built electronics packaged inside a standard CD jewel case, which synthesize an album of electronic music
- (cap) In 2005, Cantaloupe Music released 1-Bit Music, custom-built electronics packaged inside a standard CD jewel case, which synthesize an album of electronic music
- (genuine) Dutch Mistress (2013) is profiled in softening summer-hot glow, her bowl cut snappish in cantaloupe orange.
- (genuine) Hugh and Chelsea brought chips, ham-and-cheese sandwiches, cantaloupe, and Diet Pepsi.

### carboniferous  [general] 총 9 / genuine 2 (22%)
- 분포: capinit 1, cap 5, hyph 1, genuine 2
- (cap) Pinar Yoldas (TR) Carboniferous The connection between fossil fuels and plastics makes fossil fuels an immensely interesting subject to think about if one inten
- (cap) In Carboniferous I intend to connect the dots between fossil fuel and the ancient history of plants, paleobotany and problems caused by fossil fuels.
- (genuine) In August 1995, it resolves to forsake its comfortable existence as a display object and once again to expose its carboniferous granules to the whoosh and roar 
- (genuine) What Mumford called “carboniferous capitalism” involved the literal linking of the dead space of the mine, and later the oil reserve, with the world of life abo

### chine  [general] 총 9 / genuine 2 (22%)
- 분포: trunc 1, allcaps 1, cap 5, genuine 2
- (cap) Roland Flexner tells us about many trips to Japan, where the art of sumi-e (ink painting) was brought by Korean missionaries who had learned about it in China (
- (cap) Hopping out of a black cab, a Hamley’s bag in each hand, a raspberry-corduroyed Tal R was in the nick of time for a talk on Armes de Chine , at this location ei
- (genuine) Paradiso employs chine collé to layer metallic circles and ellipses over printed spreads pulled from a 1867 translation of Paradiso , the third and final chapt
- (genuine) Where an overstuffed chair, soft carpet, and draped crepe de chine seem to cover over, not least pad, the emotional terror of civic (ie.

### cutie  [general] 총 9 / genuine 2 (22%)
- 분포: allcaps 1, capinit 2, cap 4, genuine 2
- (cap) Noriko’s art during the period of the film takes the form of “Cutie and Bullie,” a hand-drawn comic from which the movie derives its title.
- (cap) Cutie and Bullie are avatars for Noriko and Ushio, and the series functions as a kind of catharsis where, on the safety of paper, Noriko can paint Cutie’s victo
- (genuine) They were hiding behind cutie culture and probably drank in secret, the little shits.
- (genuine) “It’s funny that this crowd would like something this gay,” a starstruck Scott, surrounded by even more agog middle-aged women, tells his friend Bob (Scott Baku

### duchy  [general] 총 9 / genuine 2 (22%)
- 분포: cap 7, genuine 2
- (cap) A few centuries ago, when the Sapieha Palace bustled with the aristocracy of The Grand Duchy of Lithuania, art was an integral feature of the daily life and wea
- (cap) It is part of an ensemble that encompasses the former residence of the Sapiehas – a noble family of the Grand Duchy of Lithuania – along with the Trinitarian mo
- (genuine) No article, book or exhibition fails to list the core biographical facts that tie him to West Penwith, the duchy’s westernmost tip.
- (genuine) Born Laure de Rougemont, she married Marc de Beauveau-Craon, a nobleman connected to the duchy of Lorraine, thus making her a princess.

### hyena  [general] 총 9 / genuine 2 (22%)
- 분포: allcaps 1, capinit 1, cap 3, urlish 2, genuine 2
- (cap) Mousse is happy to announce the launch of Matthew Brannon’s monograph Hyena’s Are… at Casey Kaplan, New York, on Saturday, December 10.
- (cap) At Chapter, Cardiff Havini presents a further new photographic work comprising a mural and three lightboxes, entitled Hyena (day and night).
- (genuine) The Queen —a Victorian gown in pale pink satin with a tulle crinoline and a long hyena tail—hangs from the ceiling in the dressing room, “upskirting herself,” w
- (genuine) The hyena recordings are like this too: They seem to say, “Hey, come join me.”

### jell  [general] 총 9 / genuine 2 (22%)
- 분포: cap 7, genuine 2
- (cap) Valentine’s Day Massacreand an explosion of popcorn bouncing off the screen just as the gangsters were seen being machine-gunned.Fun with Time Time, a 1977 perf
- (cap) Orange Jell-O with bananas in it, oh yes.
- (genuine) I stuck around Dia for two and a half hours, watching people converse, dance, eat, drink, and do as people do while I waited for the performance to take off, or
- (genuine) That Nelson, an enthusiastic, even reckless amateur, and Eenhoorn, a nuanced, controlled straight man, could jell into an inspired comedy team is one of the joy

### leek  [general] 총 9 / genuine 2 (22%)
- 분포: cap 6, hyph 1, genuine 2
- (cap) The gallery installation is presented in collaboration with Theaster Gates, with support from Kate Hadley Williams, Studio and Exhibitions Manager for Theaster 
- (cap) “When we move by night at the speed of desire With you at the wheel my limit goes higher Just turn me on, you turn me on You are my petrol, my drive, my dream, 
- (genuine) The outline of a leek in his hat in the infrared image suggests the effigy might also be intended as a Welshman, a sight recorded on St David’s Day by the diari
- (genuine) But a distinct leek soup?

### pitying  [general] 총 9 / genuine 2 (22%)
- 분포: hyph 7, genuine 2
- (hyph) We’re such an indulgent, whiny, self-pitying culture.
- (hyph) Baumbach’s fifth feature, unlike Margot at the Wedding, does more than just marvel at the noxious cruelty of its protagonist; Greenberg, though self-absorbed an
- (genuine) They have lost touch with their contemporaries.” The average Russian also looked upon the work with a pitying gaze: Kabakov displayed perfectly normal objects i
- (genuine) “Can’t you?” the Queen said in a pitying tone.

### quadrille  [general] 총 9 / genuine 2 (22%)
- 분포: cap 6, urlish 1, genuine 2
- (cap) As with the love rectangle of Quadrille(1938)—a reporter, a movie star, an editor, and his actress wife—there’s a frankness about sexual desires, across any bou
- (cap) For Quadrille (1975), six women appear as show ponies, in skimpy costumes with tails and shoes made from horse’s hooves, moving in formation as if in a dressage
- (genuine) Riff was a walking repository of information about Karl Marx, especially his relationship to dance (who knew he’d wooed his wife with a quadrille?).
- (genuine) Located in the quadrille del Silencio neighborhood of Milan, dense with exceptional architecture, Via Rossini 3 has a rather special pedigree.

### quarto  [general] 총 9 / genuine 2 (22%)
- 분포: allcaps 1, cap 6, genuine 2
- (cap) O Sangue ( Blood , 1989), Casa de Lava ( House of Lava , 1994), Ossos ( Bones , 1997) and, in particular, No Quarto da Vanda ( In Vanda’s Room , 2000), Juventud
- (cap) AL: I know you’re talking not only about Fontainhas, where you made three films [ Ossos ( Bones ), 1989; No Quarto da Vanda ( In Vanda’s Room ), 2000; and Juven
- (genuine) Winstanley and Son, Liverpool, on 10 October 1831, and a further forty sets were sold as lot 158, with four quarto (smaller).
- (genuine) It was only on her death, through the publication of a quarto book of her poems, that it was made public.Poems by Mrs Anne Killigrew(1686) was prefaced with a f

### shortfalls  [general] 총 9 / genuine 2 (22%)
- 분포: urlish 7, genuine 2
- (urlish) This year’s edition of Ars Electronica is an invitation to reflect on the close relationship we have developed with the digital world and how we deal with it wh
- (urlish) Late last month, its founding director, Dan Cameron,announcedthat the next iteration of the event, Prospect.2, would be postponed until the fall of 2011 from th
- (genuine) Spies is currently working to implement a new internal system that will improve communication between departments and help prevent budgeting shortfalls in the f
- (genuine) The major shortfalls faced by these young nations as they struggle to build fairer and more democratic societies amid the huge imbalances caused by an irrationa

### syndicalism  [general] 총 9 / genuine 2 (22%)
- 분포: capinit 6, hyph 1, genuine 2
- (hyph) With Spargo, I want to be clear to not reduce his critique to a moral denunciation of tactics of paralysis, or even to a flat anti-syndicalism.
- (genuine) It gives voice to art as it does to social critique, to the critique of science in the same way as the syndicalism of the old and new labour-power, to the strug
- (genuine) Spargo’s critique of sabotage is central to his attack on revolutionary syndicalism, but it has a different tenor: he argues that it “destroys the moral force o

### trotter  [general] 총 9 / genuine 2 (22%)
- 분포: capinit 1, cap 6, genuine 2
- (cap) So we might say that for Trotter, Woolf’s cinematic writing only comes to fruition after March 1926, and we have here in the case of film the kind of evidentiar
- (cap) However, rather than calling this as evidence of a direct influence on Woolf’s fiction, Trotter then ascribes it to a more diffuse atmosphere of common concern:
- (genuine) Globe trotter The journey of an artwork
- (genuine) The arch of each trotter is high, and his legs shiver, just a little.

### tweeter  [general] 총 9 / genuine 2 (22%)
- 분포: cap 6, hyph 1, genuine 2
- (cap) Key Tweeter is a performance of data nudism based on a Twitter account interfaced with a keylogger.
- (cap) on how to set up your own Key Tweeter.
- (genuine) A computer gathers all the tweets posted by the current President of the United States on one hand and by a “Love Quotes” tweeter account on the other.
- (genuine) A computer gathers all the tweets posted by the current President of the United States on one hand and by a “Love Quotes” tweeter account on the other.

### viol  [general] 총 9 / genuine 2 (22%)
- 분포: trunc 3, cap 3, urlish 1, genuine 2
- (trunc) Caio Barbiere, “UnB: arquitetos contestam monumentos ligados à violência.
- (trunc) At the exhibition at La Verrière in Brussels, many enigmatic “chambers” ( Partie Submergée , Chambre violée , Terra Platònica ) presented the vestiges of findin
- (genuine) Also seen through her limbs are a belligerent ram, a tambourine, a viol and a mask of Janus, the two-headed god.
- (genuine) I recall how thrilled the professor was by the one small figure—only a child—who has the audacity to place her foot, to lean her weight, on the bass viol, the s

### yaw  [general] 총 9 / genuine 2 (22%)
- 분포: cap 6, urlish 1, genuine 2
- (cap) In a recent number entitled “Def Si Yaw,” they attacked by name a marabout who took money from a politician during the 2000 election campaign and, in return, ca
- (cap) The PhD Critical Data Research Group currently consists of: César Escudero Andaluz, Marta Beauchamp, Hess Jeon, Gordan Savičić, Juliane Götz, Yann Patrick Marti
- (genuine) Some appeared to experience rather more roll, pitch, and yaw than others, and seemed perilously close to flying off one side where the tube becomes a strip.
- (genuine) Position and orientation (pitch, roll and yaw) is measured, as with the Eyephone, by a Polhemus sensor on the back of the hand.

### anthill  [general] 총 8 / genuine 2 (25%)
- 분포: cap 1, urlish 5, genuine 2
- (urlish) Williams endeavors to pass through the wiring of intricate networks in the case of both the internet and the anthill.
- (urlish) A certain confusion still reigns; but in a little while all will be made clear, and we shall witness at last the miracle of an animal society, the perfect and u
- (genuine) An insensate slump in the anthill also affects the best people, and must, since they think.
- (genuine) The lower floor of the gallery houses another site-specific work, Incubation place #3, in which the gallery space is dotted with anthill like conical mounds of 

### audios  [general] 총 8 / genuine 2 (25%)
- 분포: cap 1, urlish 5, genuine 2
- (urlish) Adding an exceptional length of time in comparison to common studies, in The 101-Nights we perform the recording of her sleep with 256 EEG channels, a performan
- (urlish) At the moment the project is live, receiving new testimonies and articulating a network of volunteers who take on the tasks of transcribing and translating the 
- (genuine) ToonsTunes is a musical composition that consists of four distinct movements put together by editing and looping lo-fi audios taken from Donald Duck cartoons.
- (genuine) Mini used the audios and videos of sound people made as a material to create an interactive art piece.

### checker  [general] 총 8 / genuine 2 (25%)
- 분포: cap 1, hyph 5, genuine 2
- (hyph) The IMPLEMENTOR (reality-checker) brings up objections, and makes alternate suggestions wherever reasonable, also in charge of the practical aspects of the proj
- (hyph) I was working as a fact-checker at the New Yorkerand felt lucky to have the job.
- (genuine) Among the demands of the Ciompi was the abolition of the controller, or checker – which can be associated with the ordered structure of a checkerboard grid.
- (genuine) For the title of her show, Judith Raum reduced disestablish the checker to disestablish .

### cilia  [general] 총 8 / genuine 2 (25%)
- 분포: trunc 2, cap 4, genuine 2
- (cap) Artists: Che Onejoon, Cilia Erens, Guan Xiao, Jackson Hong, Im Youngzoo, Katja Novitskova, Oriol Vilanova
- (cap) Terziev Stefan Donchev (BG) Cilia with Metal Stalks Cilia with Metal Stalks consists of an array of ­sensor wires and a small printer.
- (genuine) “I too, who was slowly reducing myself to whatever in me?was irreducible, I too had thousands of blinking cilia, and with my cilia?I move forward, I protozoan, 
- (genuine) “I too, who was slowly reducing myself to whatever in me?was irreducible, I too had thousands of blinking cilia, and with my cilia?I move forward, I protozoan, 

### colonels  [general] 총 8 / genuine 2 (25%)
- 분포: cap 6, genuine 2
- (cap) Thierry Geoffroy / Colonels aim is tocollectively develop the awareness muscle.
- (cap) This includes the period of the right-wing military junta, also called the Regime of the Colonels (1967–74), whose road to power can be traced back to the Axis 
- (genuine) In the course of her research into this convoluted history, the artist discovered the photo archive of Gert Nel, one of the former colonels of the 32nd Regiment
- (genuine) Pashas, khedives, sultans, kings, colonial proconsuls, colonels, and generals have taken turns ruling it autocratically and ruthlessly.

### ejector  [general] 총 8 / genuine 2 (25%)
- 분포: capinit 2, cap 4, genuine 2
- (cap) “Ejector is a multimedia installation that looks into the perception of reality, the body, and spirituality, weaving these elements together to understand their
- (cap) [up]Loaded Bodies: Ejector
- (genuine) It claims to be growing more powerful and personify the political life of the future, but it always gets the smallest share of ejector seats and folding elector
- (genuine) Among designer furniture, home-made constructions and sculptural objects, high chairs and ejector seats, there is room for an equally large number of job-interv

### gluten  [general] 총 8 / genuine 2 (25%)
- 분포: cap 1, hyph 3, urlish 2, genuine 2
- (hyph) “This is my first dinner of the night” hummed curator Artemis Baltoyanni while seeking some gluten-free treats (worse than finding a needle in a haystack in Ita
- (hyph) The evening’s meal was gluten-themed: fries, a lot of them, and pizza.
- (genuine) Modern industrially prepared flours do not approximate those available in the past, and the proportion of gluten (the sticky substance in flour) would be differ
- (genuine) We demonstrate real-time substance classification and validate our system with a practical case study: detecting allergens such as gluten or peanuts in food.

### handedness  [general] 총 8 / genuine 2 (25%)
- 분포: capinit 1, hyph 5, genuine 2
- (hyph) The New York poetry style is no less arrogant than any other, but this isn’t obvious to everyone at first glance because it’s a style of off-handedness and unde
- (hyph) Here, as a left-handed person, she painstakingly copied out the sentences, strictly adhering to the lines of the exercise book, in an attempt to “normalize” her
- (genuine) These changes read as keyed to the actual human form, eroding strict bilateral symmetry in favor of a subtle differentiation between left and right, or what mig
- (genuine) These reflections are expressed metaphorically in the show through the principal of chirality or ‘handedness’, a property of an object that is not superimposabl

### hymen  [general] 총 8 / genuine 2 (25%)
- 분포: capinit 2, cap 4, genuine 2
- (cap) He can flatter himself of a Conservatoire National de Bordeaux degree in electroacoustic composition and at the same time he’s fond of contemporary electronic m
- (cap) They have released albums with labels such as Shockwave, Praxis, Ant-Zen, Ad Noiseam and – of course – Hymen.
- (genuine) She was in the sealed-off halls of the CIA headquarters, in a highly protected research institute studying animal epidemics, and in an operating room in which a
- (genuine) Apart from that, it is about the screen as a hymen, the inadequacy in the depiction of transformation and about the moment of change in the image, without monta

### jabber  [general] 총 8 / genuine 2 (25%)
- 분포: cap 3, hyph 2, noneng 1, genuine 2
- (cap) I always point to the story of Jabber—which is both an .org and .com.
- (cap) In Babble, Blabber, Chatter, Gibber, Jabber, Patter, Prattle, Rattle, Yammer, Yada yada yada(2010) Pica spells out the work’s title using semaphore flags.
- (genuine) But the attraction of Europe was soon irresistible, and once in the French capital he wrote back to his Australian painting companion Tom Roberts: "The jabber o
- (genuine) The students jabber and brag about how Jewish they are: how many times they’ve been to Israel or how much money their parents donate to the temple.

### lyceum  [general] 총 8 / genuine 2 (25%)
- 분포: cap 6, genuine 2
- (cap) Having attended the opening night of Macbeth at the Lyceum Theatre on 27 December 1888, Sargent was blown away by the ‘pictorial’ power of Terry’s appearance an
- (cap) As part of this category, Arrow Rock Lyceum Theater in Missouri—the only theater between Kansas City and St.
- (genuine) Jermolaeva’s own dissidence dates to at least her time attending a conservative art lyceum, where her drawing lessons involved painting workers and collective f
- (genuine) Left intact, the Tylers’ happening Orphic lyceum became a mausoleum.

### merino  [general] 총 8 / genuine 2 (25%)
- 분포: cap 5, hyph 1, genuine 2
- (cap) The resulting multilingual poem, “txt, Is Not Written Plain,” conjures a palette of “yellow white / like the hair of my grandmother / who smokes,” “dirty pink c
- (cap) Marina Xenofontos, Holding back, holding tight , 2023, Merino wool fabric, embroidery, steel structure gallery, 330 x 150 cm 2.
- (genuine) Mix them up with a retro blazer and merino knit.
- (genuine) For DEAF2012, Meindertsma has produced five new sweaters out of wool from five merino sheep belonging to the only such flock in the Netherlands.

### molasses  [general] 총 8 / genuine 2 (25%)
- 분포: hyph 1, urlish 5, genuine 2
- (urlish) The dropper, made of hand-blown glass and resembling one half of an hourglass, is full of slowly seeping, viscous black liquid that could be mistaken for tar or
- (urlish) The bodies had become “stuck on the road with melted road-tar and molasses.
- (genuine) "They had to adapt to the disembodied reality of that thin, two-dimensional space", Rabinowitz explains, "yet their interactions had a 'thickness' determined by
- (genuine) Dillon evokes these experiences through considered materials—crystal plates cast in soap, molasses, and the scent of sweat; dried calabashes collected from Jama

### papas  [general] 총 8 / genuine 2 (25%)
- 분포: cap 5, hyph 1, genuine 2
- (cap) The master narrative, in which a limp “Papas Kino” simply shriveled up and faded away in response to the young Turks’ Oedipal uprising, has come to seem decided
- (cap) (Artistic director: Irene Papas)
- (genuine) Under the title tHE mAMAS aND tHE pAPAS , the show presents new paintings and works on paper created especially for this venue.
- (genuine) The exhibition tHE mAMAS aND tHE pAPAS unfolds on different levels: referencing the legendary American folk-rock band of the same name from the 1960s, it allude

### southerner  [general] 총 8 / genuine 2 (25%)
- 분포: cap 6, genuine 2
- (cap) HF: I could, but I thought he was some kind of Southerner.
- (cap) In the guise of Sherry, an aggressive Southerner in a flowing blonde wig, Young was offering “Sherapy” for individuals and couples, a Holiday Masturbation Works
- (genuine) But as a southerner, he well knew the delicate line he had to walk.
- (genuine) For Eustache—another southerner, raised between greater Bordeaux and the Mediterranean port of Narbonne—the artisanal model provided by Pagnol wasthething to as

### spitfire  [general] 총 8 / genuine 2 (25%)
- 분포: cap 6, genuine 2
- (cap) Michelle Vogel,Lupe Vélez: The Life and Career of Hollywood’s “Mexican Spitfire”(Jefferson, NC: McFarland, 2012), 151.
- (cap) She also has several Obies and a book adaptation of the film Rockyunder her belt—not to mention a stint wrestling as Rosa Carlo, the Mexican Spitfire.
- (genuine) Michelle and María, or M&M, were stunningly stylish; the latter was a spitfire of a Latina who resembled golden-age Mexican film starina María Félix.
- (genuine) And Malick apparently has something for Italians who drop from the sky—for instance, the flyingcircoinDays of Heavenwith its unfunnybuffoni—but whence appears M

### testers  [general] 총 8 / genuine 2 (25%)
- 분포: hyph 6, genuine 2
- (hyph) Amateur subversions and beta-testers Some people already exploit the potentially subversive possibilities of this parallel world of illicit pleasures stolen fro
- (hyph) The main players in this world are beta-testers, tweaking and adjusting reality on a day-to-day basis.
- (genuine) While developing the curriculum, I had two honest and tough beta testers and I eventually developed a program that this summer is celebrating its tenth year.
- (genuine) I don’t think we’ve had any beta testers finish it yet!

### wormwood  [general] 총 8 / genuine 2 (25%)
- 분포: cap 6, genuine 2
- (cap) What seemed to complete the cure—thoughcuremay be too positive a term for the psychological shift of replacing my own obsessive behavior with an obsession with 
- (cap) Morris makes Eric’s psychotherapeutic-collage strategy into Wormwood’s structuring principle.
- (genuine) As his investigation into what he gradually came to believe was his father’s “foul and unnatural murder” intensified and everything became “wormwood” to him, hi
- (genuine) It was made from wormwood leaves and sometimes had an alcohol content as high as 80 per cent by volume.

## E. 유지 권고 8개

사전어 + 문두 대문자/문두 소문자 위주 (희귀 보통명사 정상 표기).

  tourmaline(25) widener(25) huskies(7) wisher(7) interceptor(4) trow(4) ahoy(3) netter(3)

## F. 큐레이션 tier 정보 88개 (제거 비권고)

theme/marker/core는 의도된 키워드(고유명사 정상). 참고용.

  brazil(1770) picasso(1759) canada(1705) istanbul(1662) sharjah(1269) toronto(1262) beirut(1050) palestinian(881)
  glasgow(823) liverpool(751) freud(719) islamic(689) israeli(674) montreal(651) chile(601) americas(562)
  harlem(557) turkish(529) edinburgh(514) indonesia(509) nigeria(505) manchester(484) lebanese(469) santiago(464)
  delhi(450) syria(438) venezia(431) wales(431) colombia(428) whitechapel(418) saudi(402) gwangju(385)
  uae(379) syrian(373) qatar(354) muslim(350) salvador(348) romanian(328) romania(320) birmingham(315)
  congo(315) armenian(314) mumbai(302) senegal(301) gallen(291) ontario(288) ghana(285) kenya(281)
  indonesian(273) lagos(271) bucharest(268) mostyn(266) arabia(262) camden(261) africans(250) chilean(248)
  bristol(242) hayward(240) thames(227) islam(222) nottingham(219) sheffield(207) ussr(200) kurdish(193)
  newcastle(171) chinatown(169) ngos(169) cardiff(158) tiktok(145) argentinian(115) chicano(109) netflix(102)
  iot(97) quebec(96) ghanaian(92) kenyan(80) romani(67) latina(46) bogota(39) bipoc(33)
  maori(30) blm(14) chicana(12) afrodiasporic(6) climateaction(6) latinamerica(3) occidentalism(2) postcapitalism(1)
