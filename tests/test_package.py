from barracks_sdk import Package

reference = 'io.barracks.app';
version = '1.2.3';

def test_package_constructor():
  """
  Tests that the Package class exposes reference and version property
  """
  package = Package(reference, version)
  assert isinstance(package, Package)
  assert package.reference == reference
  assert package.version == version
