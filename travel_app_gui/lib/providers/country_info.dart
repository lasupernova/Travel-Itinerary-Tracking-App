class CountryInfo {
  // const PropertyItem({Key? key}) : super(key: key);
  String id;
  final String countryName;
  final double currencyConversion;
  final double temperature;
  final double cloudCover;
  final DateTime countryDate;

  CountryInfo(
      {this.id = "not given",
      required this.countryName,
      required this.currencyConversion,
      required this.temperature,
      required this.cloudCover,
      required this.countryDate});
}
