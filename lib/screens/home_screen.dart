import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import "package:latlong2/latlong.dart" as latLng;
import 'package:geolocator/geolocator.dart';
import 'package:app_settings/app_settings.dart';
import 'package:flutter/scheduler.dart';
import 'dart:async';
import '../services/location_service.dart';
import '../services/database_service.dart';
import '../services/preferences_service.dart';
import '../models/route.dart' as bike_route;

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late LocationService _locationService;
  final MapController _mapController = MapController();
  StreamSubscription<Position>? _positionStreamSubscription; // Para posição atual
  List<latLng.LatLng> _currentRoute = [];
  List<bike_route.Route> _savedRoutes = [];
  Map<int, List<latLng.LatLng>> _savedRoutePoints = {};
  Set<int> _selectedRouteIds = {};
  String _statusMessage = 'Pronto para gravar';
  String _distanceInfo = 'Distância: 0.00 km';
  String _pointsInfo = 'Pontos: 0';
  bool _isLoading = true;
  bool _followUserLocation = true; // Se deve seguir automaticamente a posição
  bool _isMapReady = false; // Flag para saber quando o mapa está pronto
  latLng.LatLng? _currentPosition; // Posição atual para o marcador

  @override
  void initState() {
    super.initState();
    _initializeApp();
  }

  Future<void> _initializeApp() async {
    _initializeLocationService();
    await _loadSavedRoutes();
    await _loadPreferences();
    await _getCurrentLocationAndCenter();
    _startLocationTracking(); // Inicia rastreamento contínuo de posição
    setState(() {
      _isLoading = false;
    });
  }

  void _initializeLocationService() {
    _locationService = LocationService(
      onLocationUpdate: (points) {
        setState(() {
          _currentRoute = points;
          _distanceInfo = _formatDistance(_locationService.calculateTotalDistance());
          _pointsInfo = 'Pontos: ${points.length}';
        });

        // Centralizar mapa na posição atual durante gravação
        if (_locationService.isRecording && _followUserLocation && points.isNotEmpty && _isMapReady) {
          _mapController.move(points.last, 15.0);
        }
      },
      onError: (error) {
        setState(() {
          _statusMessage = 'Erro: $error';
        });
      },
      onRouteSaved: (bike_route.Route route) {
        setState(() {
          _statusMessage = 'Rota salva: ${route.name}';
        });
        _loadSavedRoutes();
      },
    );
  }

  Future<void> _loadPreferences() async {
    await PreferencesService.instance.getUseMetric();
    // Aplicar preferências de unidades se necessário
  }

  Future<void> _getCurrentLocationAndCenter() async {
    try {
      // Verificar permissões primeiro
      bool hasPermission = await _checkLocationPermission();
      if (!hasPermission) {
        print('Sem permissão de localização');
        setState(() {
          _statusMessage = 'É necessário permitir acesso à localização';
        });
        return;
      }

      // Tentar obter posição atual com timeout (usando a nova API)
      try {
        final currentPosition = await Geolocator.getCurrentPosition(
          locationSettings: AppleSettings(
            accuracy: LocationAccuracy.high,
            timeLimit: Duration(seconds: 10),
          ),
        );
        
        print('Posição obtida: ${currentPosition.latitude}, ${currentPosition.longitude}');
        
        // Só move o mapa após o widget estar montado
        SchedulerBinding.instance.addPostFrameCallback((_) {
          if (mounted) {
            setState(() {
              _isMapReady = true;
            });
            
            _mapController.move(
              latLng.LatLng(currentPosition.latitude, currentPosition.longitude),
              16.0,
            );
          }
        });
        
        setState(() {
          _statusMessage = 'Localização obtida com sucesso';
        });
      } catch (e) {
        print('Timeout ao obter posição atual, tentando última posição conhecida: $e');
        
        // Fallback para última posição conhecida
        final lastPosition = await _locationService.getLastKnownPosition();
        if (lastPosition != null) {
          print('Última posição conhecida: ${lastPosition.latitude}, ${lastPosition.longitude}');
          
          SchedulerBinding.instance.addPostFrameCallback((_) {
            if (mounted) {
              setState(() {
                _isMapReady = true;
              });
              
              _mapController.move(
                latLng.LatLng(lastPosition.latitude, lastPosition.longitude),
                16.0,
              );
            }
          });
          
          setState(() {
            _statusMessage = 'Usando última posição conhecida';
          });
        } else {
          print('Nenhuma posição disponível, mantendo posição padrão');
          setState(() {
            _statusMessage = 'Não foi possível obter sua localização';
          });
        }
      }
    } catch (e) {
      print('Erro geral ao obter posição: $e');
      setState(() {
        _statusMessage = 'Erro ao obter localização: $e';
      });
    }
  }

  Future<bool> _checkLocationPermission() async {
    // Verificar se serviço de localização está habilitado
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      print('Serviço de localização desabilitado');
      // Oferecer abrir configurações
      _showLocationServiceDisabledDialog();
      return false;
    }

    // Verificar permissões
    LocationPermission permission = await Geolocator.checkPermission();
    
    if (permission == LocationPermission.denied) {
      print('Permissão negada, solicitando...');
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        print('Permissão negada pelo usuário');
        return false;
      }
    }
    
    if (permission == LocationPermission.deniedForever) {
      print('Permissão negada permanentemente');
      // Oferecer abrir configurações do sistema
      _showOpenSettingsDialog();
      return false;
    }
    
    if (permission == LocationPermission.whileInUse) {
      print('Permissão concedida: enquanto em uso');
    }
    
    print('Permissão concedida: $permission');
    return true;
  }

  void _showLocationServiceDisabledDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Serviço de Localização Desativado'),
        content: Text('O serviço de localização está desativado. Para usar o app, você precisa ativar o serviço de localização.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              AppSettings.openAppSettings();
            },
            child: Text('Abrir Configurações'),
          ),
        ],
      ),
    );
  }

  void _showOpenSettingsDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Permissão de Localização'),
        content: Text('A permissão de localização foi negada permanentemente. Para usar o app, você precisa permitir o acesso à localização nas configurações do sistema.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              AppSettings.openAppSettings();
            },
            child: Text('Abrir Configurações'),
          ),
        ],
      ),
    );
  }

  void _toggleFollowLocation() {
    setState(() {
      _followUserLocation = !_followUserLocation;
    });

    if (_followUserLocation && _currentRoute.isNotEmpty && _isMapReady) {
      _mapController.move(_currentRoute.last, 15.0);
    }
  }

  void _startLocationTracking() async {
    // Inicia rastreamento contínuo de posição para o marcador atual
    try {
      final hasPermission = await _checkLocationPermission();
      if (!hasPermission) return;

      _positionStreamSubscription = Geolocator.getPositionStream(
        locationSettings: AppleSettings(
          accuracy: LocationAccuracy.high,
          distanceFilter: 10, // Atualiza a cada 10 metros
        ),
      ).listen((Position position) {
        setState(() {
          _currentPosition = latLng.LatLng(position.latitude, position.longitude);
        });

        // Seguir automaticamente se estiver habilitado
        if (_followUserLocation && _isMapReady) {
          _mapController.move(
            latLng.LatLng(position.latitude, position.longitude),
            16.0,
          );
        }
      });
    } catch (e) {
      print('Erro ao iniciar rastreamento de posição: $e');
    }
  }

  void _stopLocationTracking() {
    _positionStreamSubscription?.cancel();
    _positionStreamSubscription = null;
  }

  Future<void> _loadSavedRoutes() async {
    try {
      final routes = await DatabaseService.instance.getAllRoutes();
      setState(() {
        _savedRoutes = routes;
        // Adicionar automaticamente todas as rotas à seleção
        _selectedRouteIds = routes.map((r) => r.id!).toSet();
      });

      // Carregar pontos de todas as rotas automaticamente
      for (final route in routes) {
        await _loadRoutePoints(route.id!);
      }
    } catch (e) {
      print('Erro ao carregar rotas: $e');
    }
  }

  Future<void> _loadRoutePoints(int routeId) async {
    try {
      final points = await DatabaseService.instance.getRoutePoints(routeId);
      setState(() {
        _savedRoutePoints[routeId] = points
            .map((p) => latLng.LatLng(p.latitude, p.longitude))
            .toList();
      });
    } catch (e) {
      print('Erro ao carregar pontos da rota $routeId: $e');
    }
  }

  String _formatDistance(double distanceInMeters) {
    final useMetric = true; // Pode vir das preferências
    if (useMetric) {
      if (distanceInMeters < 1000) {
        return '${distanceInMeters.toStringAsFixed(0)} m';
      } else {
        return '${(distanceInMeters / 1000).toStringAsFixed(2)} km';
      }
    } else {
      final distanceInMiles = distanceInMeters * 0.000621371;
      if (distanceInMiles < 1) {
        return '${(distanceInMeters * 3.28084).toStringAsFixed(0)} ft';
      } else {
        return '${distanceInMiles.toStringAsFixed(2)} mi';
      }
    }
  }

  Future<void> _toggleRecording() async {
    if (_locationService.isRecording) {
      _locationService.stopRecording();

      if (_currentRoute.isNotEmpty) {
        _showSaveDialog();
      } else {
        setState(() {
          _statusMessage = 'Gravação parada (sem pontos)';
        });
      }
    } else {
      final success = await _locationService.startRecording();
      if (success) {
        setState(() {
          _statusMessage = 'Gravando...';
        });
      } else {
        setState(() {
          _statusMessage = 'Falha ao iniciar gravação';
        });
      }
    }
  }

  void _showSaveDialog() {
    final controller = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Salvar Rota'),
        content: TextField(
          controller: controller,
          decoration: InputDecoration(
            hintText: 'Nome da rota',
            labelText: 'Nome',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _clearRoute();
            },
            child: Text('Descartar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _saveRoute(controller.text);
            },
            child: Text('Salvar'),
          ),
        ],
      ),
    );
  }

  Future<void> _saveRoute(String name) async {
    final routeName = name.trim().isEmpty ? 'Percurso sem nome' : name.trim();
    await _locationService.saveRoute(name: routeName);
    _clearRoute();
  }

  void _clearRoute() {
    _locationService.clearRecordedPoints();
    setState(() {
      _currentRoute = [];
      _distanceInfo = 'Distância: 0.00 km';
      _pointsInfo = 'Pontos: 0';
      _statusMessage = 'Rota limpa';
    });
  }

  Future<void> _deleteRoute(int routeId) async {
    await DatabaseService.instance.deleteRoute(routeId);

    _loadSavedRoutes();
  }

  Color _getRouteColor(int index) {
    final colors = [
      Colors.blue,
      Colors.red,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.teal,
      Colors.pink,
      Colors.amber,
      Colors.cyan,
      Colors.indigo,
    ];
    return colors[index % colors.length];
  }

  @override
  void dispose() {
    _locationService.dispose();
    _stopLocationTracking();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Pedal Around the World'),
        actions: [
          IconButton(
            icon: Icon(
              _followUserLocation ? Icons.gps_fixed : Icons.gps_not_fixed,
              color: _followUserLocation ? Colors.green : null,
            ),
            onPressed: () {
              _toggleFollowLocation();
              // Tenta obter posição novamente quando clica no GPS
              _getCurrentLocationAndCenter();
            },
            tooltip: _followUserLocation ? 'Seguir localização' : 'Não seguir localização',
          ),
          IconButton(
            icon: Icon(Icons.bar_chart),
            onPressed: () {
              Navigator.pushNamed(context, '/statistics');
            },
            tooltip: 'Estatísticas',
          ),
          IconButton(
            icon: Icon(Icons.list),
            onPressed: _showSavedRoutes,
            tooltip: 'Rotas salvas',
          ),
          IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {
              Navigator.pushNamed(context, '/settings');
            },
            tooltip: 'Configurações',
          ),
          IconButton(
            icon: Icon(Icons.delete_outline),
            onPressed: _clearRoute,
            tooltip: 'Limpar rota',
          ),
        ],
      ),
      body: Column(
        children: [
          _buildStatusBar(),
          Expanded(child: _buildMap()),
        ],
      ),
      floatingActionButton: _buildRecordingButton(),
    );
  }

  Widget _buildStatusBar() {
    return Container(
      padding: EdgeInsets.all(16),
      color: Colors.blue.shade50,
      child: Column(
        children: [
          Text(
            _statusMessage,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.blue.shade800,
            ),
          ),
          SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text(
                _distanceInfo,
                style: TextStyle(fontSize: 14),
              ),
              Text(
                _pointsInfo,
                style: TextStyle(fontSize: 14),
              ),
              if (_selectedRouteIds.isNotEmpty)
                Text(
                  '${_selectedRouteIds.length} rota(s) no mapa',
                  style: TextStyle(fontSize: 14, color: Colors.green),
                ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMap() {
    return FlutterMap(
      mapController: _mapController,
      options: MapOptions(
        initialCenter: latLng.LatLng(51.5, -0.09),
        initialZoom: 13.0,
      ),
      children: [
        TileLayer(
            urlTemplate: "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
            subdomains: ['a', 'b', 'c', 'd'],
            userAgentPackageName: 'com.vitoralcantara.pedal_around_the_world'),
        // Mostrar rotas salvas selecionadas
        ..._selectedRouteIds.map((routeId) {
          final index = _savedRoutes.indexWhere((r) => r.id == routeId);
          final points = _savedRoutePoints[routeId] ?? [];
          final color = _getRouteColor(index);

          if (points.isEmpty) return SizedBox.shrink();

          return PolylineLayer(
            polylines: [
              Polyline(
                points: points,
                color: color,
                strokeWidth: 3.0,
              ),
            ],
          );
        }).toList(),
        // Mostrar rota sendo gravada
        if (_currentRoute.isNotEmpty)
          PolylineLayer(
            polylines: [
              Polyline(
                points: _currentRoute,
                color: Colors.black,
                strokeWidth: 4.0,
              ),
            ],
          ),
        // Marcador da posição atual (sempre visível)
        if (_currentPosition != null)
          MarkerLayer(
            markers: [
              Marker(
                width: 30.0,
                height: 30.0,
                point: _currentPosition!,
                child: Container(
                  child: Icon(
                    Icons.my_location,
                    color: Colors.red,
                    size: 30,
                  ),
                ),
              ),
            ],
          ),
        // Marcadores da rota atual
        if (_currentRoute.isNotEmpty)
          MarkerLayer(
            markers: [
              Marker(
                width: 40.0,
                height: 40.0,
                point: _currentRoute.first,
                child: Container(
                  child: Icon(
                    Icons.location_on,
                    color: Colors.green,
                    size: 40,
                  ),
                ),
              ),
              Marker(
                width: 40.0,
                height: 40.0,
                point: _currentRoute.last,
                child: Container(
                  child: Icon(
                    Icons.directions_bike,
                    color: Colors.black,
                    size: 40,
                  ),
                ),
              ),
            ],
          ),
      ],
    );
  }

  Widget _buildRecordingButton() {
    return FloatingActionButton(
      onPressed: _toggleRecording,
      tooltip: _locationService.isRecording ? 'Parar gravação' : 'Iniciar gravação',
      backgroundColor: _locationService.isRecording ? Colors.red : Colors.green,
      child: Icon(
        _locationService.isRecording ? Icons.stop : Icons.play_arrow,
      ),
    );
  }

  void _showSavedRoutes() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Container(
        height: MediaQuery.of(context).size.height * 0.7,
        child: Column(
          children: [
            _buildRoutesHeader(),
            Expanded(child: _buildRoutesList()),
          ],
        ),
      ),
    );
  }

  Widget _buildRoutesHeader() {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        border: Border(bottom: BorderSide(color: Colors.grey.shade300)),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Rotas Salvas',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              Text('${_savedRoutes.length} rotas'),
            ],
          ),
          Padding(
            padding: EdgeInsets.only(top: 8),
            child: Text(
              'Todas as rotas sempre visíveis no mapa',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRoutesList() {
    if (_savedRoutes.isEmpty) {
      return Center(
        child: Text(
          'Nenhuma rota salva ainda',
          style: TextStyle(color: Colors.grey),
        ),
      );
    }

    return ListView.builder(
      itemCount: _savedRoutes.length,
      itemBuilder: (context, index) {
        final route = _savedRoutes[index];
        final routeColor = _getRouteColor(index);

        return ListTile(
          leading: Icon(Icons.directions_bike, color: routeColor),
          title: Row(
            children: [
              Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(
                  color: routeColor,
                  shape: BoxShape.circle,
                ),
              ),
              SizedBox(width: 8),
              Expanded(
                child: Text(route.name),
              ),
            ],
          ),
          subtitle: Text(
            '${route.formattedDistance} • ${route.formattedDuration}',
          ),
          trailing: Text(route.formattedDate),
          onLongPress: () {
            Navigator.of(context).pop();
            _showRouteDetails(route);
          },
        );
      },
    );
  }

  void _showRouteDetails(bike_route.Route route) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(route.name),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Distância: ${route.formattedDistance}'),
            Text('Duração: ${route.formattedDuration}'),
            Text('Data: ${route.formattedDate}'),
            Text('Pontos: ${route.pointCount}'),
            SizedBox(height: 16),
            Row(
              children: [
                Icon(
                  Icons.visibility,
                  color: Colors.green,
                  size: 16,
                ),
                SizedBox(width: 8),
                Text(
                  'Visível no mapa',
                  style: TextStyle(
                    color: Colors.green,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Fechar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _showDeleteRouteDialog(route);
            },
            child: Text('Excluir', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  void _showDeleteRouteDialog(bike_route.Route route) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Excluir Rota'),
        content: Text('Deseja excluir a rota "${route.name}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _deleteRoute(route.id!);
            },
            child: Text('Excluir', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}
