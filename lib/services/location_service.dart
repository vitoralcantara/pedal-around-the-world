import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart' as latLng;
import '../models/route.dart';
import '../models/route_point.dart';
import 'database_service.dart';

class LocationService {
  StreamSubscription<Position>? _positionStreamSubscription;
  final List<latLng.LatLng> _recordedPoints = [];
  final List<DateTime> _timestamps = []; // Para armazenar timestamps dos pontos
  final Function(List<latLng.LatLng>)? onLocationUpdate;
  final Function(String)? onError;
  final Function(Route)? onRouteSaved;
  bool _isRecording = false;
  DateTime _recordingStartTime = DateTime.now();
  
  // Configurações de localização otimizadas para ciclismo
  final LocationSettings _locationSettings = const LocationSettings(
    accuracy: LocationAccuracy.high,
    distanceFilter: 10, // 10 metros entre pontos
  );

  LocationService({
    this.onLocationUpdate,
    this.onError,
    this.onRouteSaved,
  });

  bool get isRecording => _isRecording;
  List<latLng.LatLng> get recordedPoints => List.unmodifiable(_recordedPoints);
  int get pointCount => _recordedPoints.length;

  /// Verifica se os serviços de localização estão habilitados
  Future<bool> checkLocationService() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      onError?.call('Os serviços de localização estão desabilitados.');
      return false;
    }
    return true;
  }

  /// Verifica e solicita permissões de localização
  Future<bool> checkPermissions() async {
    LocationPermission permission = await Geolocator.checkPermission();
    
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        onError?.call('Permissões de localização negadas.');
        return false;
      }
    }
    
    if (permission == LocationPermission.deniedForever) {
      onError?.call('Permissões de localização negadas permanentemente.');
      return false;
    }
    
    return true;
  }

  /// Inicia o rastreamento de localização
  Future<bool> startRecording() async {
    if (_isRecording) {
      return true;
    }

    // Verificar serviços de localização
    if (!await checkLocationService()) {
      return false;
    }

    // Verificar permissões
    if (!await checkPermissions()) {
      return false;
    }

    try {
      // Limpar pontos anteriores e inicializar timestamp
      _recordedPoints.clear();
      _timestamps.clear();
      _recordingStartTime = DateTime.now();

      // Iniciar stream de localização
      _positionStreamSubscription = Geolocator.getPositionStream(
        locationSettings: _locationSettings,
      ).listen(
        (Position position) {
          final point = latLng.LatLng(
            position.latitude,
            position.longitude,
          );
          final timestamp = DateTime.now();

          _recordedPoints.add(point);
          _timestamps.add(timestamp);
          onLocationUpdate?.call(_recordedPoints);
        },
        onError: (error) {
          onError?.call('Erro ao obter localização: $error');
          stopRecording();
        },
      );

      _isRecording = true;
      return true;
    } catch (e) {
      onError?.call('Erro ao iniciar rastreamento: $e');
      return false;
    }
  }

  /// Para o rastreamento de localização
  void stopRecording() {
    if (_positionStreamSubscription != null) {
      _positionStreamSubscription!.cancel();
      _positionStreamSubscription = null;
    }
    _isRecording = false;
  }

  /// Limpa os pontos gravados
  void clearRecordedPoints() {
    _recordedPoints.clear();
    _timestamps.clear();
  }

  /// Calcula a duração da gravação (em segundos)
  int getRecordingDuration() {
    if (_timestamps.isEmpty) {
      return 0;
    }
    if (_timestamps.length == 1) {
      return DateTime.now().difference(_recordingStartTime).inSeconds;
    }
    return _timestamps.last.difference(_timestamps.first).inSeconds;
  }

  /// Salva a rota atual no banco de dados
  Future<Route?> saveRoute({String name = 'Percurso sem nome'}) async {
    if (_recordedPoints.isEmpty) {
      onError?.call('Não há pontos para salvar.');
      return null;
    }

    try {
      final distance = calculateTotalDistance();
      final duration = getRecordingDuration();
      final date = DateTime.now();

      // Criar objeto Route
      final route = Route(
        name: name,
        date: date,
        distance: distance,
        duration: duration,
        pointCount: _recordedPoints.length,
      );

      // Criar lista de RoutePoint
      final routePoints = <RoutePoint>[];
      for (int i = 0; i < _recordedPoints.length; i++) {
        routePoints.add(RoutePoint(
          routeId: 0, // Será definido pelo banco de dados
          latitude: _recordedPoints[i].latitude,
          longitude: _recordedPoints[i].longitude,
          timestamp: _timestamps.isNotEmpty ? _timestamps[i] : date,
        ));
      }

      // Salvar no banco de dados
      final routeId = await DatabaseService.instance.saveRouteWithPoints(route, routePoints);

      // Atualizar o route com o ID gerado
      final savedRoute = route.copyWith(id: routeId);

      onRouteSaved?.call(savedRoute);

      return savedRoute;
    } catch (e) {
      onError?.call('Erro ao salvar rota: $e');
      return null;
    }
  }

  /// Calcula a distância total do percurso (em metros)
  double calculateTotalDistance() {
    if (_recordedPoints.length < 2) {
      return 0.0;
    }

    double totalDistance = 0.0;
    for (int i = 1; i < _recordedPoints.length; i++) {
      totalDistance += Geolocator.distanceBetween(
        _recordedPoints[i - 1].latitude,
        _recordedPoints[i - 1].longitude,
        _recordedPoints[i].latitude,
        _recordedPoints[i].longitude,
      );
    }

    return totalDistance;
  }

  /// Obtém a última localização conhecida
  Future<Position?> getLastKnownPosition() async {
    try {
      return await Geolocator.getLastKnownPosition();
    } catch (e) {
      onError?.call('Erro ao obter última localização: $e');
      return null;
    }
  }

  /// Dispose do serviço
  void dispose() {
    stopRecording();
    _recordedPoints.clear();
    _timestamps.clear();
  }
}
