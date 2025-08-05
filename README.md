# Délibérations.be (Plonemeeting Portal)


<img src="https://raw.githubusercontent.com/IMIO/buildout.pm.portal/refs/heads/master/.github/img/logo.svg" width="200" />

Deliberations.be is a web application for citizens to consult official deliberations and publications from local authorities in Wallonia (Belgium). Built on the open-source Plone CMS and integrated with the iA.Delib deliberation management system, it streamlines administrative workflows and ensures compliance with regional legislation.


## Features

* **Citizen Access**: Browse deliberations and official publications from Walloon local authorities.
* **Advanced Search**: Filter by keywords, dates, and categories for precise results.
* **eIDAS Timestamping**: Manage publications with qualified electronic timestamps.
* **Workflow Automation**: Integration with [iA.Délib](https://github.com/IMIO/buildout.pm.git) for automated deliberation processes.
* **Document Generation**: Automatically generate publication-ready documents.
* **Multi-Tenancy**: Separate user and role management for each entity with customizable themes.

## Requirements

* **Plone CMS**: ≥ 6.1
* **Python**: ≥ 3.12
* **Buildout**: Installed in your environment

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/IMIO/buildout.pm.portal.git
   cd buildout.pm.portal
   ```

2. **Bootstrap Buildout**:

   ```bash
   python3 -m venv .
   bin/pip install -r requirements.txt
   ```

3. **Configure Buildout**:

   Edit `buildout.cfg` to adjust settings as needed (e.g., database connection, add-ons,...).

4. **Run Buildout**:

   ```bash
   bin/buildout
   ```

5. **Start the Plone Instance**:

   ```bash
   bin/instance fg
   ```

   By default, the site will be available at `http://localhost:8080`.

## Documentation

User documentation is available at [iA.Delib Documentation](https://docs.imio.be/iadelib/deliberations.be).

## Screenshots

![Deliberations.be screenshot](https://raw.githubusercontent.com/IMIO/buildout.pm.portal/refs/heads/master/.github/img/screenshot_home.jpg)
![Deliberations.be screenshot](https://raw.githubusercontent.com/IMIO/buildout.pm.portal/refs/heads/master/.github/img/screenshot_publication.jpg)
![Deliberations.be screenshot](https://raw.githubusercontent.com/IMIO/buildout.pm.portal/refs/heads/master/.github/img/screenshot_deliberation.jpg)
![Deliberations.be screenshot](https://raw.githubusercontent.com/IMIO/buildout.pm.portal/refs/heads/master/.github/img/screenshot_meeting.jpg)


## Maintenance & Support

* **Support iA.Delib**: [support-delib@imio.be](mailto:support-delib@imio.be)
* **Project Contact**: Antoine Duchêne ([antoine.duchene@imio.be](mailto:antoine.duchene@imio.be))

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow Plone coding standards and update relevant documentation.

## License

This project is licensed under the GNU GPL-2.0. See the [LICENSE](https://github.com/IMIO/buildout.pm.portal/blob/master/LICENSE) file for details.
