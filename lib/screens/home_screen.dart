import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import "package:latlong2/latlong.dart" as latLng;
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
  List<latLng.LatLng> _currentRoute = [];
  List<bike_route.Route> _savedRoutes = [];
  Map<int, List<latLng.LatLng>> _savedRoutePoints = {};
  Set<int> _selectedRouteIds = {};
  String _statusMessage = 'Pronto para gravar';
  String _distanceInfo = 'Distância: 0.00 km';
  String _pointsInfo = 'Pontos: 0';
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initializeApp();
  }

  Future<void> _initializeApp() async {
    _initializeLocationService();
    await _loadSavedRoutes();
    await _loadPreferences();
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

  Future<void> _loadSavedRoutes() async {
    try {
      final routes = await DatabaseService.instance.getAllRoutes();
      setState(() {
        _savedRoutes = routes;
      });

      for (final routeId in _selectedRouteIds) {
        await _loadRoutePoints(routeId);
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

    setState(() {
      _selectedRouteIds.remove(routeId);
      _savedRoutePoints.remove(routeId);
    });

    _loadSavedRoutes();
  }

  Future<void> _toggleRouteSelection(int routeId) async {
    setState(() {
      if (_selectedRouteIds.contains(routeId)) {
        _selectedRouteIds.remove(routeId);
        _savedRoutePoints.remove(routeId);
      } else {
        _selectedRouteIds.add(routeId);
      }
    });

    if (_selectedRouteIds.contains(routeId)) {
      await _loadRoutePoints(routeId);
    }
  }

  void _clearRouteSelection() {
    setState(() {
      _selectedRouteIds.clear();
      _savedRoutePoints.clear();
    });
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
              Row(
                children: [
                  if (_selectedRouteIds.isNotEmpty)
                    TextButton(
                      onPressed: () {
                        _clearRouteSelection();
                        Navigator.of(context).pop();
                      },
                      child: Text('Limpar seleção'),
                    ),
                  Text('${_savedRoutes.length} rotas'),
                ],
              ),
            ],
          ),
          if (_selectedRouteIds.isNotEmpty)
            Padding(
              padding: EdgeInsets.only(top: 8),
              child: Text(
                '${_selectedRouteIds.length} rota(s) selecionada(s) para visualização',
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
        final isSelected = _selectedRouteIds.contains(route.id!);
        final routeColor = _getRouteColor(index);

        return ListTile(
          leading: Checkbox(
            value: isSelected,
            onChanged: (value) {
              _toggleRouteSelection(route.id!);
            },
            activeColor: routeColor,
          ),
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
          onTap: () {
            _toggleRouteSelection(route.id!);
          },
          onLongPress: () {
            Navigator.of(context).pop();
            _showRouteDetails(route);
          },
        );
      },
    );
  }

  void _showRouteDetails(bike_route.Route route) {
    final isSelected = _selectedRouteIds.contains(route.id!);

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
                  isSelected ? Icons.visibility : Icons.visibility_off,
                  color: isSelected ? Colors.green : Colors.grey,
                  size: 16,
                ),
                SizedBox(width: 8),
                Text(
                  isSelected ? 'Visível no mapa' : 'Não visível no mapa',
                  style: TextStyle(
                    color: isSelected ? Colors.green : Colors.grey,
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
              _toggleRouteSelection(route.id!);
            },
            child: Text(isSelected ? 'Ocultar' : 'Mostrar no mapa'),
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
