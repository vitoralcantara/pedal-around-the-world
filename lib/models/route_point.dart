class RoutePoint {
  final int? id;
  final int routeId;
  final double latitude;
  final double longitude;
  final DateTime timestamp;

  RoutePoint({
    this.id,
    required this.routeId,
    required this.latitude,
    required this.longitude,
    required this.timestamp,
  });

  // Converte RoutePoint para Map para salvar no banco de dados
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'routeId': routeId,
      'latitude': latitude,
      'longitude': longitude,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  // Cria RoutePoint a partir de Map do banco de dados
  factory RoutePoint.fromMap(Map<String, dynamic> map) {
    return RoutePoint(
      id: map['id'] as int?,
      routeId: map['routeId'] as int,
      latitude: map['latitude'] as double,
      longitude: map['longitude'] as double,
      timestamp: DateTime.parse(map['timestamp'] as String),
    );
  }

  // Converte para LatLng do latlong2
  toLatLng() {
    // Importar latlong2: import 'package:latlong2/latlong.dart' as latLng;
    // return latLng.LatLng(latitude, longitude);
    // Por enquanto retorna um Map para evitar dependência circular
    return {'latitude': latitude, 'longitude': longitude};
  }
}
