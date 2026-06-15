class Route {
  final int? id;
  final String name;
  final DateTime date;
  final double distance; // em metros
  final int duration; // em segundos
  final int pointCount;

  Route({
    this.id,
    required this.name,
    required this.date,
    required this.distance,
    required this.duration,
    required this.pointCount,
  });

  // Converte Route para Map para salvar no banco de dados
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'date': date.toIso8601String(),
      'distance': distance,
      'duration': duration,
      'pointCount': pointCount,
    };
  }

  // Cria Route a partir de Map do banco de dados
  factory Route.fromMap(Map<String, dynamic> map) {
    return Route(
      id: map['id'] as int?,
      name: map['name'] as String,
      date: DateTime.parse(map['date'] as String),
      distance: map['distance'] as double,
      duration: map['duration'] as int,
      pointCount: map['pointCount'] as int,
    );
  }

  // Cópia de Route com alguns campos alterados
  Route copyWith({
    int? id,
    String? name,
    DateTime? date,
    double? distance,
    int? duration,
    int? pointCount,
  }) {
    return Route(
      id: id ?? this.id,
      name: name ?? this.name,
      date: date ?? this.date,
      distance: distance ?? this.distance,
      duration: duration ?? this.duration,
      pointCount: pointCount ?? this.pointCount,
    );
  }

  // Formata a distância para exibição
  String get formattedDistance {
    if (distance < 1000) {
      return '${distance.toStringAsFixed(0)} m';
    } else {
      return '${(distance / 1000).toStringAsFixed(2)} km';
    }
  }

  // Formata a duração para exibição
  String get formattedDuration {
    final hours = duration ~/ 3600;
    final minutes = (duration % 3600) ~/ 60;
    final seconds = duration % 60;

    if (hours > 0) {
      return '${hours}h ${minutes}min';
    } else if (minutes > 0) {
      return '${minutes}min ${seconds}s';
    } else {
      return '${seconds}s';
    }
  }

  // Formata a data para exibição
  String get formattedDate {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inDays == 0) {
      return 'Hoje, ${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';
    } else if (difference.inDays == 1) {
      return 'Ontem, ${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} dias atrás';
    } else {
      return '${date.day}/${date.month}/${date.year}';
    }
  }
}
