from netlab_ai.parser import analyze_text

def test_extracts_numbered_questions():
    practice = analyze_text("1. ¿Qué es una VLAN?\n2. Configure dos VLAN en el switch.")
    assert len(practice.activities) == 2
    assert practice.activities[0].kind == "pregunta"

def test_page_number_is_preserved():
    practice = analyze_text("[PÁGINA 2]\n1. Explique qué es DHCP.")
    assert practice.activities[0].page == 2

def test_empty_text_is_valid():
    practice = analyze_text("")
    assert practice.activities == []
