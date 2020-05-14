from missing_addresses import compute_complete_address_diff
import os
from pathlib import Path


script_path = Path(__file__).parent.absolute()


def test_compute_complete_address_diff():
    os.chdir(Path(script_path, '..', 'PaperTown'))
    Path('missing_addresses.osm').unlink(missing_ok=True)
    Path('street_ordered_html_summary.html').unlink(missing_ok=True)
    compute_complete_address_diff('Leonberg', None)
    assert Path('missing_addresses.osm').exists()
    assert Path('street_ordered_html_summary.html').exists()
