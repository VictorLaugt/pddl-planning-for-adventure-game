(define (problem map) (:domain exploration-game)
    (:objects
        p - player
        ps1 - location
        fond_de_la_mine - location
        jungle_profonde - location
        cabane_perchee - location
        bunker - location
        corde - item
        pied_du_volcan - location
        crevasse - location
        parapente - item
        violon - item
        flechette - item
        epave - location
        trois_cairns - location
        cale - location
        sommet_du_volcan - location
        ruines - location
        pelle - item
        choice_sentier - choice
        repere_des_pirates - location
        cabane_du_pêcheur - location
        tente_du_chef - location
        ps2 - location
        feu_de_camp - location
        lac - location
        conduit_d_aeration - location
        porte_principale - location
        atelier - location
        plage - location
        baobab - location
        canne_a_pêche - item
        rocher_de_la_tortue - location
        grand_totem - location
        symbole_bouteille - item
        infirmerie - location
        fond_du_puits - location
        machette - item
        riviere - location
        choice_feu_de_camp - choice
        milieu_du_lac - location
        enceinte - item
        ilot_des_pirates - location
        rhum - item
        flute - item
        mine_abandonnee - location
        roue - item
        cratere - location
        tipis - location
        horizon - location
        ration - item
        symbole_coffre - item
        temple_maya - location
        jungle - location
        campement_des_indigenes - location
        sentier - location
        voile - item
        cascade - location
        puits - location
    )

    (:init
        (is_at p feu_de_camp)
        (connected cabane_perchee riviere)
        (connected sommet_du_volcan cratere)
        (connected cratere infirmerie)
        (connected cabane_du_pêcheur infirmerie)
        (possible_collect_if rocher_de_la_tortue rhum canne_a_pêche)
        (connected baobab jungle)
        (possible_collect pied_du_volcan machette)
        (connected_if campement_des_indigenes tipis flechette)
        (connected ilot_des_pirates epave)
        (connected epave cale)
        (connected fond_de_la_mine mine_abandonnee)
        (connected tente_du_chef grand_totem)
        (connected cabane_du_pêcheur rocher_de_la_tortue)
        (connected infirmerie atelier)
        (connected horizon cabane_perchee)
        (offers choice_feu_de_camp flechette)
        (connected epave grand_totem)
        (connected_if grand_totem atelier ration)
        (possible_collect cratere roue)
        (connected_if jungle jungle_profonde machette)
        (connected plage cabane_du_pêcheur)
        (connected campement_des_indigenes tente_du_chef)
        (connected pied_du_volcan puits)
        (connected_if sommet_du_volcan ilot_des_pirates parapente)
        (connected ps1 bunker)
        (connected infirmerie plage)
        (connected tipis atelier)
        (connected feu_de_camp sentier)
        (possible_choice feu_de_camp choice_feu_de_camp)
        (connected porte_principale atelier)
        (connected mine_abandonnee pied_du_volcan)
        (connected ps2 bunker)
        (possible_collect milieu_du_lac symbole_bouteille)
        (connected ruines crevasse)
        (possible_collect_if tente_du_chef flute enceinte)
        (possible_collect ilot_des_pirates violon)
        (connected rocher_de_la_tortue cabane_du_pêcheur)
        (connected rocher_de_la_tortue plage)
        (connected_if riviere conduit_d_aeration flute)
        (offers choice_feu_de_camp ration)
        (connected epave plage)
        (connected puits atelier)
        (connected trois_cairns riviere)
        (connected_if temple_maya lac flechette)
        (connected trois_cairns ruines)
        (connected pied_du_volcan sommet_du_volcan)
        (connected riviere cascade)
        (possible_collect ilot_des_pirates machette)
        (connected porte_principale jungle)
        (connected jungle campement_des_indigenes)
        (connected lac riviere)
        (possible_collect_if horizon rhum ration)
        (connected conduit_d_aeration bunker)
        (connected grand_totem rocher_de_la_tortue)
        (connected atelier porte_principale)
        (connected porte_principale crevasse)
        (possible_collect jungle_profonde symbole_coffre)
        (possible_collect_if_2 atelier parapente corde voile)
        (connected atelier plage)
        (connected puits pied_du_volcan)
        (connected grand_totem infirmerie)
        (connected sommet_du_volcan atelier)
        (possible_collect baobab machette)
        (connected jungle atelier)
        (possible_collect crevasse rhum)
        (connected_if fond_du_puits ps2 symbole_bouteille)
        (connected infirmerie jungle)
        (possible_collect infirmerie flechette)
        (connected lac crevasse)
        (connected_if puits fond_du_puits corde)
        (connected_if ilot_des_pirates ps1 symbole_coffre)
        (connected cascade jungle)
        (connected_if riviere conduit_d_aeration violon)
        (connected plage baobab)
        (connected jungle temple_maya)
        (connected riviere pied_du_volcan)
        (connected_if lac milieu_du_lac canne_a_pêche)
        (connected lac campement_des_indigenes)
        (connected pied_du_volcan mine_abandonnee)
        (possible_choice sentier choice_sentier)
        (offers choice_sentier rhum)
        (possible_collect_if cascade rhum canne_a_pêche)
        (connected plage epave)
        (possible_collect cabane_du_pêcheur canne_a_pêche)
        (connected pied_du_volcan riviere)
        (connected baobab cabane_perchee)
        (connected rocher_de_la_tortue jungle)
        (connected tipis infirmerie)
        (connected crevasse pied_du_volcan)
        (possible_collect_if horizon corde ration)
        (connected infirmerie baobab)
        (connected repere_des_pirates cale)
        (connected cale epave)
        (connected jungle porte_principale)
        (connected plage repere_des_pirates)
        (connected_if porte_principale bunker pelle)
        (connected porte_principale puits)
        (possible_collect epave voile)
        (connected trois_cairns puits)
        (connected temple_maya riviere)
        (connected cabane_perchee horizon)
        (offers choice_sentier corde)
        (connected fond_du_puits puits)
        (connected sentier trois_cairns)
        (connected atelier jungle)
        (offers choice_feu_de_camp corde)
        (possible_collect cabane_perchee ration)
        (connected cabane_perchee baobab)
        (connected cabane_perchee infirmerie)
        (connected jungle_profonde jungle)
        (connected milieu_du_lac lac)
        (connected rocher_de_la_tortue repere_des_pirates)
        (connected crevasse ruines)
        (connected baobab tente_du_chef)
    )

    (:goal (and
        (is_at p bunker)
    ))
)
