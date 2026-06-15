import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/route.dart';
import '../models/route_point.dart';

class DatabaseService {
  static final DatabaseService instance = DatabaseService._init();
  static Database? _database;

  DatabaseService._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('bike_routes.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createTables,
    );
  }

  Future<void> _createTables(Database db, int version) async {
    // Tabela de rotas
    await db.execute('''
      CREATE TABLE routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        distance REAL NOT NULL,
        duration INTEGER NOT NULL,
        pointCount INTEGER NOT NULL
      )
    ''');

    // Tabela de pontos das rotas
    await db.execute('''
      CREATE TABLE route_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        routeId INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (routeId) REFERENCES routes (id) ON DELETE CASCADE
      )
    ''');

    // Criar índices para melhorar performance
    await db.execute('CREATE INDEX idx_route_points_routeId ON route_points(routeId)');
    await db.execute('CREATE INDEX idx_routes_date ON routes(date)');
  }

  // ============================================
  // OPERAÇÕES COM ROTAS
  // ============================================

  // Insere uma nova rota
  Future<int> insertRoute(Route route) async {
    final db = await database;
    return await db.insert('routes', route.toMap());
  }

  // Atualiza uma rota existente
  Future<int> updateRoute(Route route) async {
    final db = await database;
    return await db.update(
      'routes',
      route.toMap(),
      where: 'id = ?',
      whereArgs: [route.id],
    );
  }

  // Deleta uma rota (e seus pontos em cascata)
  Future<int> deleteRoute(int id) async {
    final db = await database;
    return await db.delete(
      'routes',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // Busca uma rota por ID
  Future<Route?> getRouteById(int id) async {
    final db = await database;
    final maps = await db.query(
      'routes',
      where: 'id = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty) {
      return Route.fromMap(maps.first);
    }
    return null;
  }

  // Busca todas as rotas, ordenadas por data (mais recentes primeiro)
  Future<List<Route>> getAllRoutes() async {
    final db = await database;
    final result = await db.query(
      'routes',
      orderBy: 'date DESC',
    );
    return result.map((map) => Route.fromMap(map)).toList();
  }

  // Busca rotas por data
  Future<List<Route>> getRoutesByDate(DateTime startDate, DateTime endDate) async {
    final db = await database;
    final result = await db.query(
      'routes',
      where: 'date BETWEEN ? AND ?',
      whereArgs: [startDate.toIso8601String(), endDate.toIso8601String()],
      orderBy: 'date DESC',
    );
    return result.map((map) => Route.fromMap(map)).toList();
  }

  // ============================================
  // OPERAÇÕES COM PONTOS DE ROTA
  // ============================================

  // Insere múltiplos pontos de uma vez (para performance)
  Future<void> insertRoutePoints(List<RoutePoint> points) async {
    final db = await database;
    final batch = db.batch();

    for (final point in points) {
      batch.insert('route_points', point.toMap());
    }

    await batch.commit(noResult: true);
  }

  // Insere um único ponto
  Future<int> insertRoutePoint(RoutePoint point) async {
    final db = await database;
    return await db.insert('route_points', point.toMap());
  }

  // Busca todos os pontos de uma rota
  Future<List<RoutePoint>> getRoutePoints(int routeId) async {
    final db = await database;
    final result = await db.query(
      'route_points',
      where: 'routeId = ?',
      whereArgs: [routeId],
      orderBy: 'timestamp ASC',
    );
    return result.map((map) => RoutePoint.fromMap(map)).toList();
  }

  // Deleta todos os pontos de uma rota
  Future<int> deleteRoutePoints(int routeId) async {
    final db = await database;
    return await db.delete(
      'route_points',
      where: 'routeId = ?',
      whereArgs: [routeId],
    );
  }

  // ============================================
  // OPERAÇÕES COMBINADAS
  // ============================================

  // Salva uma rota completa com seus pontos
  Future<int> saveRouteWithPoints(Route route, List<RoutePoint> points) async {
    final db = await database;
    
    // Inicia transação
    return await db.transaction((txn) async {
      // Insere a rota
      final routeId = await txn.insert('routes', route.toMap());
      
      // Insere os pontos com o routeId correto
      final pointsWithRouteId = points.map((point) {
        return RoutePoint(
          routeId: routeId,
          latitude: point.latitude,
          longitude: point.longitude,
          timestamp: point.timestamp,
        );
      }).toList();
      
      // Insere os pontos em batch
      final batch = txn.batch();
      for (final point in pointsWithRouteId) {
        batch.insert('route_points', point.toMap());
      }
      await batch.commit(noResult: true);
      
      return routeId;
    });
  }

  // Busca uma rota completa com seus pontos
  Future<Map<String, dynamic>?> getRouteWithPoints(int routeId) async {
    final route = await getRouteById(routeId);
    if (route == null) return null;

    final points = await getRoutePoints(routeId);

    return {
      'route': route,
      'points': points,
    };
  }

  // Busca todas as rotas com contagem de pontos
  Future<List<Map<String, dynamic>>> getRoutesWithPointCount() async {
    final db = await database;
    final result = await db.rawQuery('''
      SELECT r.*, COUNT(rp.id) as actualPointCount
      FROM routes r
      LEFT JOIN route_points rp ON r.id = rp.routeId
      GROUP BY r.id
      ORDER BY r.date DESC
    ''');

    return result.map((map) {
      final route = Route.fromMap(map);
      return {
        'route': route,
        'actualPointCount': map['actualPointCount'] as int,
      };
    }).toList();
  }

  // ============================================
  // UTILITÁRIOS
  // ============================================

  // Retorna estatísticas gerais
  Future<Map<String, dynamic>> getStatistics() async {
    final db = await database;

    final totalRoutes = await db.rawQuery('SELECT COUNT(*) as count FROM routes');
    final totalDistance = await db.rawQuery('SELECT SUM(distance) as total FROM routes');
    final totalDuration = await db.rawQuery('SELECT SUM(duration) as total FROM routes');
    final totalPoints = await db.rawQuery('SELECT COUNT(*) as count FROM route_points');

    return {
      'totalRoutes': totalRoutes.first['count'] as int,
      'totalDistance': totalDistance.first['total'] as double? ?? 0.0,
      'totalDuration': totalDuration.first['total'] as int? ?? 0,
      'totalPoints': totalPoints.first['count'] as int,
    };
  }

  // Limpa todo o banco de dados (cuidado ao usar!)
  Future<void> clearDatabase() async {
    final db = await database;
    await db.delete('route_points');
    await db.delete('routes');
  }

  // Fecha o banco de dados
  Future<void> close() async {
    final db = await database;
    await db.close();
    _database = null;
  }
}
