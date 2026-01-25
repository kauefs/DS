import       pytest,         os
from streamlit.testing.v1 import AppTest
PATH  =os.path.join(os.path.dirname(__file__),'..','tourismBR.py')
@pytest.fixture(scope="module")
def shared( ):
    'Initialize StreamLit AppTest once per module, speeding up testing.'
    at=AppTest.from_file(PATH, default_timeout=45)
    at.run( )
    return at
def test_app_smoke(shared):
    'Basic smoke test to ensure the app starts and loads data.'
   #at=AppTest.from_file(PATH, default_timeout=45)
   #at.run( )
    # Assert no exceptions occurred during run:
    assert not shared.exception
    # Assert Title exists:
    assert     shared.title[0].value=='Brazil 🇧🇷 InterNational Tourist Arrivals'
def test_sidebar_info(shared):
    'Check if sidebar contains the expected branding and info.'
   #at=AppTest.from_file(PATH)
   #at.run( )
    # Check SideBar title:
    assert     shared.sidebar.title  [0].value=='ƊⱭȾɅViƧi🧿Ƞ&trade;'
    # Check if the year slider exists:
    assert len(shared.sidebar.slider)>0
    assert     shared.sidebar.slider [0].label=='Year Range'
def test_kpi_metrics(shared):
    'Verify KPI metrics are rendered.'
   #at=AppTest.from_file(PATH)
   #at.run( )
    # Ensure all three metrics are present:
    assert len                (shared.metric)>=3
    # Check first metric label:
    assert 'Total Arrivals' in shared.metric  [0].label
