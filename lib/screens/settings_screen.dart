import 'package:flutter/material.dart';
import '../services/preferences_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _useMetric = true;
  String _locationAccuracy = 'high';
  int _distanceFilter = 10;
  String _mapStyle = 'streets';
  bool _enableNotifications = true;
  bool _autoSaveRoutes = false;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    final useMetric = await PreferencesService.instance.getUseMetric();
    final locationAccuracy = await PreferencesService.instance.getLocationAccuracy();
    final distanceFilter = await PreferencesService.instance.getDistanceFilter();
    final mapStyle = await PreferencesService.instance.getMapStyle();
    final enableNotifications = await PreferencesService.instance.getEnableNotifications();
    final autoSaveRoutes = await PreferencesService.instance.getAutoSaveRoutes();

    setState(() {
      _useMetric = useMetric;
      _locationAccuracy = locationAccuracy;
      _distanceFilter = distanceFilter;
      _mapStyle = mapStyle;
      _enableNotifications = enableNotifications;
      _autoSaveRoutes = autoSaveRoutes;
      _isLoading = false;
    });
  }

  Future<void> _savePreferences() async {
    await PreferencesService.instance.setUseMetric(_useMetric);
    await PreferencesService.instance.setLocationAccuracy(_locationAccuracy);
    await PreferencesService.instance.setDistanceFilter(_distanceFilter);
    await PreferencesService.instance.setMapStyle(_mapStyle);
    await PreferencesService.instance.setEnableNotifications(_enableNotifications);
    await PreferencesService.instance.setAutoSaveRoutes(_autoSaveRoutes);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Configurações')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Configurações'),
      ),
      body: ListView(
        children: [
          _buildSectionHeader('Unidades de Medida'),
          _buildMetricToggle(),
          Divider(),
          _buildSectionHeader('Configurações de GPS'),
          _buildLocationAccuracyDropdown(),
          _buildDistanceFilterSlider(),
          Divider(),
          _buildSectionHeader('Configurações de Mapa'),
          _buildMapStyleDropdown(),
          Divider(),
          _buildSectionHeader('Funcionalidades'),
          _buildNotificationsToggle(),
          _buildAutoSaveToggle(),
          Divider(),
          _buildSectionHeader('Dados'),
          _buildClearDataButton(),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: EdgeInsets.all(16),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: Colors.grey,
        ),
      ),
    );
  }

  Widget _buildMetricToggle() {
    return SwitchListTile(
      title: Text('Sistema Métrico'),
      subtitle: Text('Usar km/m em vez de mi/ft'),
      value: _useMetric,
      onChanged: (value) {
        setState(() {
          _useMetric = value;
        });
        _savePreferences();
      },
    );
  }

  Widget _buildLocationAccuracyDropdown() {
    return ListTile(
      title: Text('Precisão do GPS'),
      subtitle: Text(_getAccuracyLabel(_locationAccuracy)),
      trailing: DropdownButton<String>(
        value: _locationAccuracy,
        items: [
          DropdownMenuItem(value: 'low', child: Text('Baixa')),
          DropdownMenuItem(value: 'medium', child: Text('Média')),
          DropdownMenuItem(value: 'high', child: Text('Alta')),
          DropdownMenuItem(value: 'best', child: Text('Melhor')),
        ],
        onChanged: (value) {
          if (value != null) {
            setState(() {
              _locationAccuracy = value;
            });
            _savePreferences();
          }
        },
      ),
    );
  }

  String _getAccuracyLabel(String accuracy) {
    switch (accuracy) {
      case 'low':
        return 'Baixa economia de bateria';
      case 'medium':
        return 'Equilibrado';
      case 'high':
        return 'Alta precisão';
      case 'best':
        return 'Melhor precisão (consome bateria)';
      default:
        return 'Desconhecido';
    }
  }

  Widget _buildDistanceFilterSlider() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Filtro de distância: $_distanceFilter metros'),
          Slider(
            value: _distanceFilter.toDouble(),
            min: 5,
            max: 50,
            divisions: 9,
            label: '$_distanceFilter m',
            onChanged: (value) {
              setState(() {
                _distanceFilter = value.round();
              });
              _savePreferences();
            },
          ),
          Text(
            'Menor valor = mais pontos, maior precisão',
            style: TextStyle(fontSize: 12, color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildMapStyleDropdown() {
    return ListTile(
      title: Text('Estilo do Mapa'),
      subtitle: Text(_getMapStyleLabel(_mapStyle)),
      trailing: DropdownButton<String>(
        value: _mapStyle,
        items: [
          DropdownMenuItem(value: 'streets', child: Text('Ruas')),
          DropdownMenuItem(value: 'satellite', child: Text('Satélite')),
          DropdownMenuItem(value: 'terrain', child: Text('Terreno')),
          DropdownMenuItem(value: 'dark', child: Text('Escuro')),
        ],
        onChanged: (value) {
          if (value != null) {
            setState(() {
              _mapStyle = value;
            });
            _savePreferences();
          }
        },
      ),
    );
  }

  String _getMapStyleLabel(String style) {
    switch (style) {
      case 'streets':
        return 'Mapa de ruas';
      case 'satellite':
        return 'Imagem de satélite';
      case 'terrain':
        return 'Terreno';
      case 'dark':
        return 'Tema escuro';
      default:
        return 'Desconhecido';
    }
  }

  Widget _buildNotificationsToggle() {
    return SwitchListTile(
      title: Text('Notificações'),
      subtitle: Text('Receber notificações do app'),
      value: _enableNotifications,
      onChanged: (value) {
        setState(() {
          _enableNotifications = value;
        });
        _savePreferences();
      },
    );
  }

  Widget _buildAutoSaveToggle() {
    return SwitchListTile(
      title: Text('Auto-Salvar Rotas'),
      subtitle: Text('Salvar automaticamente ao parar gravação'),
      value: _autoSaveRoutes,
      onChanged: (value) {
        setState(() {
          _autoSaveRoutes = value;
        });
        _savePreferences();
      },
    );
  }

  Widget _buildClearDataButton() {
    return ListTile(
      title: Text(
        'Limpar Todos os Dados',
        style: TextStyle(color: Colors.red),
      ),
      subtitle: Text('Excluir todas as rotas e configurações'),
      trailing: Icon(Icons.delete, color: Colors.red),
      onTap: () {
        _showClearDataDialog();
      },
    );
  }

  void _showClearDataDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Limpar Todos os Dados'),
        content: Text('Tem certeza que deseja excluir todas as rotas e redefinir as configurações? Esta ação não pode ser desfeita.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () async {
              Navigator.of(context).pop();
              await _clearAllData();
            },
            child: Text('Limpar', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  Future<void> _clearAllData() async {
    try {
      // Limpar preferências
      await PreferencesService.instance.clearAll();
      
      // Limpar banco de dados
      // await DatabaseService.instance.clearDatabase();
      
      // Recarregar preferências
      await _loadPreferences();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Dados limpos com sucesso')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erro ao limpar dados: $e')),
      );
    }
  }
}
