import  pandas              as   pd
from streamlit.testing.v1 import AppTest
def test_app_smoke( ):
    'Basic smoke test to ensure the app starts and loads data'
    at=AppTest.from_file('TourismBR.py', default_timeout=30)
    at.run( )
    # Assert no exceptions occurred during run:
    assert not at.exception
    # Assert Title exists:
    assert at.title[0].value=='Brazil 🇧🇷 InterNational Tourist Arrivals'
def test_sidebar_info( ):
    'Check if sidebar contains the expected branding and info'
    at=AppTest.from_file('TourismBR.py')
    at.run( )
    # Check SideBar title:
    assert at.sidebar.title[0].value=='ƊⱭȾɅViƧi🧿Ƞ&trade;'
    # Check if the year slider exists:
    assert len(at.sidebar.slider)>0
    assert at.sidebar.slider[0].label=='Year Range'
def test_kpi_metrics( ):
    'Verify that KPI metrics are rendered'
    at=AppTest.from_file('TourismBR.py')
    at.run( )
    # Ensure all three metrics are present:
    assert len(at.metric)>=3
    # Check first metric label:
    assert 'Total Arrivals' in at.metric[0].label
