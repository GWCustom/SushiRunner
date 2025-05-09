<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/GWCustom/SushiRunner">
    <img src="https://drive.google.com/uc?export=view&id=1_RekqDx9tOY-4ziZLn7cG9sozMXIhrfE" alt="Logo" width="80" height="50.6">
  </a>

<h3 align="center">SushiRunner</h3>

<p align="center">
  A Dash interface to submit Sushi applications via B-Fabric using SushiFabric and WorkflowManager.
  <br />
  <br />
  <a href="https://github.com/GWCustom/SushiRunner/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
  ·
  <a href="https://github.com/GWCustom/SushiRunner/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>
</div>

> **Note**: This project is built using the [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps) library and was forked from the [bfabric-web-app-template](https://github.com/GWCustom/bfabric-web-app-template).

---

## About

**SushiRunner** is a web-based interface for submitting [Sushi](https://github.com/uzh/sushi) applications using [B-Fabric](https://fgcz-bfabric.uzh.ch/bfabric/) datasets as input. It bridges the B-Fabric LIMS system with the [SushiFabric](https://github.com/uzh/sushi_fabric) command-line interface and the [WorkflowManager](https://github.com/uzh/workflow_manager) execution engine.

This app allows users to:
- Load dataset metadata from B-Fabric
- Configure Sushi application parameters through a Dash-based UI
- Generate the required `dataset.tsv` and `parameters.tsv` files
- Submit jobs to the Sushi infrastructure without needing to manually write scripts

> This app is intended as a **proof-of-concept**, showcasing generalized support for Sushi-based execution workflows directly from the B-Fabric environment.

---

## Key Features

- Dash UI for selecting and configuring Sushi apps
- Generic + app-specific parameter forms (RAM, cores, options, etc.)
- TSV generation for Sushi input
- Seamless B-Fabric authentication and dataset loading
- Job submission via `sushi_fabric` (no Redis dependency)
- Optional project charging and reporting integration

---

## Workflow Overview

1. **User launches app from a B-Fabric dataset page**
2. **Dataset metadata is automatically loaded**
3. **User configures the job parameters**
4. **`dataset.tsv` and `parameters.tsv` are generated**
5. **`sushi_fabric` is invoked with the appropriate class and args**
6. **WorkflowManager handles execution, monitoring, and completion emails**
7. **Workunits and logs are updated in B-Fabric**

---

## Example Applications

Each Sushi app is defined as a standalone Dash module. For example:

- **[FastqcApp](https://github.com/GWCustom/SushiRunner/blob/main/FastqcApp.py)** supports:
  - Generic inputs: RAM, cores, partition, etc.
  - App-specific toggles: `paired`, `showNativeReports`, etc.
  - Table-based dataset preview
  - Dynamic job submission via `run_main_job`

Other supported applications follow a similar structure and can be added modularly.

---

## Useful Resources

- [Sushi Documentation](https://github.com/uzh/sushi)
- [Sushi App Example - FastQC](https://github.com/uzh/sushi/blob/master/master/lib/FastqcApp.rb)
- [SushiFabric](https://github.com/uzh/sushi_fabric)
- [WorkflowManager](https://github.com/uzh/workflow_manager)
- [EZRun R Package](https://github.com/uzh/ezRun)
- [FGCZ Sushi Job Monitor](https://fgcz-sushi.uzh.ch/job_monitoring)

---

## Built With

- [Dash](https://dash.plotly.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Plotly](https://plotly.com/)
- [bfabric-web-apps](https://github.com/GWCustom/bfabric-web-apps)
- [SushiFabric](https://github.com/uzh/sushi_fabric)
- [WorkflowManager](https://github.com/uzh/workflow_manager)

---

## Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/GWCustom/SushiRunner.git
cd SushiRunner
```

### 2. Create and Activate a Virtual Environment

#### Using `virtualenv` (Linux/Mac):

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Using `virtualenv` (Windows):

```bash
python -m venv venv
venv\Scripts\activate
```

#### Or using `conda`:

```bash
conda create -n sushi-runner pip
conda activate sushi-runner
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.bfabricpy.yml`

Create this file in your home directory (`~/.bfabricpy.yml`):

```yaml
GENERAL:
  default_config: PRODUCTION

PRODUCTION:
  login: your_username
  password: your_password
  base_url: https://your-bfabric-api-endpoint
```

### 5. Run the App

```bash
python3 index.py
```

Visit [http://localhost:8050](http://localhost:8050) in your browser.

---

## License

Distributed under the MIT License. See [LICENSE](https://github.com/GWCustom/SushiRunner/blob/main/LICENSE) for details.

---

## Contact

GWC GmbH – [GitHub](https://github.com/GWCustom)  
Griffin White – [LinkedIn](https://www.linkedin.com/in/griffin-white-3aa20918a/)  
Marc Zuber – [LinkedIn](https://www.linkedin.com/in/marc-zuber-1161b3305/)
