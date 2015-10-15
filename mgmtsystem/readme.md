Migration du module

Création des dossiers models et views
Déplacements des fichiers board_mgmtsystem_view.xml, menu.xml et mgmtsystem_system.xml dans views
Renommage de board_mgmtsystem_view.xml en board_mgmtsystem.xml
Déplacements des fichiers mgmtsystem_system.py dans models

Opération effectué dans la vue board_mgmtsystem.xml

Retrait dans board_mgmtsystem_form du code

<hpaned>
    <child1>
    </child1>
    <child2>
    </child2>
</hpaned>

à l'intérieur de la balise form

Opération effectué dans la vue menu.xml

Retrait dans menuitem menu_mgmtsystem_root des paramêtres

web_icon="images/mgmtsystem.png"
web_icon_hover="images/mgmtsystem-hover.png"

modification du fichier __openerp_.py afin qu'il reflète les différents chemin des fichiers
