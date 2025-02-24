# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl / Based on: Risk Model Canvas
# © 2023 by Gilbert van Zeijl and Vincent van Dijk is licensed under CC BY-SA 4.0
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemRiskCanvas(models.Model):
    """Risk Analyses Canvas"""

    _name = "mgmtsystem.risk.canvas"
    _description = "Risk Model Canvas"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Canvas Name', required=True)
    system_id = fields.Many2one('mgmtsystem.system', 'System', required=True)
    company_id = fields.Many2one('res.company', 'Company', related="system_id.company_id", store=True)

    # Just add HTML fields to add the list of risks in the canvas.
    # Todo: Maybe link them later to hazards?
    risks_key_partners = fields.Html(
        string='Key Partners', translate=False,
        help='De bouwsteen kern partners gaat over het netwerk van leveranciers en partners die '
             'nodig zijn om het businessmodel te laten werken. Bedrijven gaan om allerlei redenen '
             'partnerschappen aan. Het creëren van het juiste netwerk kan als een belangrijke factor '
             'voor succesvol ondernemerschap gezien worden. Een oude wijsheid luidt niet voor niks: '
             '-Het geheel is meer dan de som der delen-. Partners kunnen een organisatie helpen om '
             'dingen te doen die alleen niet mogelijk zijn. De juiste partnerships helpen om '
             'succesvol te zijn, te groeien en te concurreren.'
    )
    risks_key_activities = fields.Html(
        string='Key Activities', translate=False,
        help='In de bouwsteen kernactiviteiten worden de belangrijkste activiteiten beschreven '
              'die een onderneming nodig heeft om goed te presteren. Het gaat dus om de '
              'kernactiviteiten die de organisatie moet uitvoeren om de waardepropositie te '
              'realiseren, klanten te bereiken, klantrelaties te onderhouden en inkomsten te verdienen. '
              'Welke activiteiten dit zijn hangt compleet af van de inrichting van het businessmodel'
    )
    risks_key_resources = fields.Html(
        string='Key Resources', translate=False,
        help='De key resources Business Model Canvas bouwsteen beschrijft de belangrijkste middelen'
             'die nodig zijn om de waardepropositie te kunnen realiseren en het businessmodel te laten '
             'werken. Key resources kunnen in eigendom zijn van het bedrijf, '
             'maar kunnen ook geleased worden of bij key partners verkregen worden. '
             'Key resources kunnen in de volgende categorieën worden ingedeeld: fysiek, financieel, '
             'intellectueel en menselijk (human resources).'
    )
    risks_key_value_prop = fields.Html(
        string='Key Value Proposition', translate=False,
        help='De ”Waardeproposities” vormt de kern van je bedrijf. Richt je op de waarde die je voor '
             'je klanten creëert, de belofte aan je klanten; dat is meer dan een opsomming van '
             'producten. Wat is de kern van je product aanbod, welke elementen zijn uniek'
    )
    risks_key_cust_relations = fields.Html(
        string='Key Customer Relations', translate=False,
        help='In de bouwsteen ”klantrelaties” wordt er beschreven hoe de onderneming in contact '
             'staat met de klant en hoe relaties opgebouwd en onderhouden worden met ieder '
             'klantsegment. Er zijn verschillende type relaties die men aan kan gaan met klanten. '
             'Voor een onderneming is het belangrijk om te motiveren waarom men een bepaalde relatie '
             'aan wil gaan met een klantsegment. De keuze van het type klantrelatie heeft namelijk '
             'invloed op alles wat een bedrijf doet en beïnvloedt ook de andere bouwstenen in het '
             'Business Model Canvas. Er zijn de volgende soorten klantrelaties te onderscheiden: '
             'Persoonlijke relatie, digitale relatie, community, co-creatie en zelfservice.'
    )
    risks_key_cust_segments = fields.Html(
        string='Key Customer Segments', translate=False,
        help='Wie zijn je klanten? De meeste bedrijven richten zich op een deel van de markt; '
             'op één of meerdere segmenten.'
    )
    risks_key_channels = fields.Html(
        string='Key Channels', translate=False,
        help='Met kanalen worden al de manieren waarmee een organisatie in contact staat met de '
             'klant bedoeld. Het vinden van de juiste mix van kanalen is cruciaal om klanten met de '
             'waardepropositie te bereiken. In de bouwsteen kanalen beschrijf je hoe je bedrijf met '
             'de verschillende klanten communiceert en hoe je deze klanten met de waardepropositie '
             'bereikt. De manieren hoe men in contact staat met de klant kunnen op diverse manieren '
             'onderverdeeld worden. Zo is er onderscheidt te maken in communicatie-, distributie- en '
             'verkoopkanalen. Ook kan er onderscheidt gemaakt worden tussen online- en fysieke '
             'kanalen.'
    )
    risks_key_costs = fields.Html(
        string='Cost structure', translate=False,
        help='De bouwsteen kostenstructuur beschrijft al de belangrijke kosten die gemaakt worden '
             'bij het uitvoeren van een businessmodel. Kosten zijn onvermijdbaar! Het creëren van '
             'waarde, het onderhouden van klantrelaties en het genereren van inkomsten brengen '
             'allemaal kosten met zich mee. Zoals vanzelfsprekend is het belangrijk om de kosten '
             'binnen de perken te houden en te focussen op zaken die daadwerkelijk waarde toevoegen '
             'voor klanten. Voor het ene businessmodel is kostenreductie één van de belangrijkste '
             'zaken, terwijl dit in andere businessmodellen minder belangrijk is'
    )
    risks_key_income = fields.Html(
        string='Income structure', translate=False,
        help='Om als bedrijf levensvatbaar te zijn moet het voldoende inkomsten genereren. De '
             'inkomsten die een bedrijf genereert moeten hoog genoeg zijn om de kosten te dekken en '
             'onder aan de streep een mooi bedrijfsresultaat(winst) over te houden. Een bedrijf '
             'zonder goed verdienmodel is gedoemd te falen! De kassa moet rinkelen, want een druppelende '
             'geldkraan is niet genoeg om te overleven.'
    )

    def action_open_risks(self):
        return {
            'name': 'Risks (Canvas)',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model':'mgmtsystem.hazard',
            'target': 'current',
            'views': [(False, 'tree'),(False, 'form')]
        }
