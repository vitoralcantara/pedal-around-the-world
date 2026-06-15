import 'package:shared_preferences/shared_preferences.dart';

class PreferencesService {
  static final PreferencesService instance = PreferencesService._init();
  static SharedPreferences? _prefs;

  PreferencesService._init();

  Future<SharedPreferences> get prefs async {
    _prefs ??= await SharedPreferences.getInstance();
    return _prefs!;
  }

  // Unidades de medida
  static const String _keyUseMetric = 'use_metric';
  
  Future<bool> getUseMetric() async {
    final pref = await prefs;
    return pref.getBool(_keyUseMetric) ?? true; // Default: metric
  }

  Future<void> setUseMetric(bool value) async {
    final pref = await prefs;
    await pref.setBool(_keyUseMetric, value);
  }

  // Configurações de GPS
  static const String _keyLocationAccuracy = 'location_accuracy';
  
  Future<String> getLocationAccuracy() async {
    final pref = await prefs;
    return pref.getString(_keyLocationAccuracy) ?? 'high'; // Default: high
  }

  Future<void> setLocationAccuracy(String value) async {
    final pref = await prefs;
    await pref.setString(_keyLocationAccuracy, value);
  }

  static const String _keyDistanceFilter = 'distance_filter';
  
  Future<int> getDistanceFilter() async {
    final pref = await prefs;
    return pref.getInt(_keyDistanceFilter) ?? 10; // Default: 10 metros
  }

  Future<void> setDistanceFilter(int value) async {
    final pref = await prefs;
    await pref.setInt(_keyDistanceFilter, value);
  }

  // Configurações de mapa
  static const String _keyMapStyle = 'map_style';
  
  Future<String> getMapStyle() async {
    final pref = await prefs;
    return pref.getString(_keyMapStyle) ?? 'streets'; // Default: streets
  }

  Future<void> setMapStyle(String value) async {
    final pref = await prefs;
    await pref.setString(_keyMapStyle, value);
  }

  // Notificações
  static const String _keyEnableNotifications = 'enable_notifications';
  
  Future<bool> getEnableNotifications() async {
    final pref = await prefs;
    return pref.getBool(_keyEnableNotifications) ?? true; // Default: enabled
  }

  Future<void> setEnableNotifications(bool value) async {
    final pref = await prefs;
    await pref.setBool(_keyEnableNotifications, value);
  }

  // Auto-save
  static const String _keyAutoSaveRoutes = 'auto_save_routes';
  
  Future<bool> getAutoSaveRoutes() async {
    final pref = await prefs;
    return pref.getBool(_keyAutoSaveRoutes) ?? false; // Default: disabled
  }

  Future<void> setAutoSaveRoutes(bool value) async {
    final pref = await prefs;
    await pref.setBool(_keyAutoSaveRoutes, value);
  }

  // Limpar todas as preferências
  Future<void> clearAll() async {
    final pref = await prefs;
    await pref.clear();
  }
}
