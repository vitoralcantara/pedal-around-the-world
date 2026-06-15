import 'package:flutter/material.dart';
import '../services/database_service.dart';
import '../models/route.dart' as bike_route;

class StatisticsScreen extends StatefulWidget {
  const StatisticsScreen({Key? key}) : super(key: key);

  @override
  _StatisticsScreenState createState() => _StatisticsScreenState();
}

class _StatisticsScreenState extends State<StatisticsScreen> {
  Map<String, dynamic> _statistics = {};
  List<bike_route.Route> _recentRoutes = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadStatistics();
  }

  Future<void> _loadStatistics() async {
    try {
      final stats = await DatabaseService.instance.getStatistics();
      final routes = await DatabaseService.instance.getAllRoutes();
      
      // Pegar as 5 rotas mais recentes
      final recent = routes.take(5).toList();

      setState(() {
        _statistics = stats;
        _recentRoutes = recent;
        _isLoading = false;
      });
    } catch (e) {
      print('Erro ao carregar estatísticas: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Estatísticas')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Estatísticas'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildOverviewCards(),
            _buildDetailedStats(),
            _buildRecentRoutes(),
          ],
        ),
      ),
    );
  }

  Widget _buildOverviewCards() {
    final totalRoutes = _statistics['totalRoutes'] as int? ?? 0;
    final totalDistance = _statistics['totalDistance'] as double? ?? 0.0;
    final totalDuration = _statistics['totalDuration'] as int? ?? 0;
    final totalPoints = _statistics['totalPoints'] as int? ?? 0;

    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Visão Geral',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 16),
          GridView.count(
            crossAxisCount: 2,
            shrinkWrap: true,
            physics: NeverScrollableScrollPhysics(),
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            children: [
              _buildStatCard(
                'Rotas',
                totalRoutes.toString(),
                Icons.route,
                Colors.blue,
              ),
              _buildStatCard(
                'Distância Total',
                _formatDistance(totalDistance),
                Icons.straighten,
                Colors.green,
              ),
              _buildStatCard(
                'Tempo Total',
                _formatDuration(totalDuration),
                Icons.access_time,
                Colors.orange,
              ),
              _buildStatCard(
                'Pontos GPS',
                _formatNumber(totalPoints),
                Icons.gps_fixed,
                Colors.purple,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      padding: EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 32),
          SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          SizedBox(height: 4),
          Text(
            title,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey[600],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailedStats() {
    final totalRoutes = _statistics['totalRoutes'] as int? ?? 0;
    final totalDistance = _statistics['totalDistance'] as double? ?? 0.0;
    final totalDuration = _statistics['totalDuration'] as int? ?? 0;

    if (totalRoutes == 0) {
      return SizedBox.shrink();
    }

    final avgDistance = totalDistance / totalRoutes;
    final avgDuration = (totalDuration / totalRoutes).round();

    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Médias',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 16),
          Card(
            child: ListTile(
              leading: Icon(Icons.route, color: Colors.blue),
              title: Text('Distância Média por Rota'),
              trailing: Text(_formatDistance(avgDistance)),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.access_time, color: Colors.orange),
              title: Text('Duração Média por Rota'),
              trailing: Text(_formatDuration(avgDuration)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecentRoutes() {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Rotas Recentes',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 16),
          if (_recentRoutes.isEmpty)
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  'Nenhuma rota registrada ainda',
                  style: TextStyle(color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
              ),
            )
          else
            ..._recentRoutes.map((route) => Card(
              child: ListTile(
                leading: Icon(Icons.directions_bike, color: Colors.green),
                title: Text(route.name),
                subtitle: Text(
                  '${route.formattedDistance} • ${route.formattedDuration}',
                ),
                trailing: Text(route.formattedDate),
                onTap: () {
                  // Navegar para detalhes da rota se necessário
                },
              ),
            )).toList(),
        ],
      ),
    );
  }

  String _formatDistance(double distanceInMeters) {
    if (distanceInMeters < 1000) {
      return '${distanceInMeters.toStringAsFixed(0)} m';
    } else {
      return '${(distanceInMeters / 1000).toStringAsFixed(2)} km';
    }
  }

  String _formatDuration(int seconds) {
    final hours = seconds ~/ 3600;
    final minutes = (seconds % 3600) ~/ 60;

    if (hours > 0) {
      return '${hours}h ${minutes}min';
    } else {
      return '${minutes}min';
    }
  }

  String _formatNumber(int number) {
    if (number >= 1000) {
      return '${(number / 1000).toStringAsFixed(1)}k';
    }
    return number.toString();
  }
}
