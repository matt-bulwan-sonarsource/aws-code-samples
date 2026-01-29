## **Title: RCA: INC0022222- AWS outage causing Users Lambda/Service Failure in US on Oct 20th 2025**

### **Incident Impact (how external or internal users were impacted):** SonarCloud US was down for the majority of the day and the EU instance was blocked from deploying. Internally we had a code freeze to avoid having broken deployments.

**Sonar Customer Impacting:** Y

---

**Triggered By (what triggered the incident):**

Many alarms including many P1s were triggered and it was first flagged by the User lambda

---

**Was this issue detected through monitoring? Y/N**

* Yes, many P3, P2 and P1s were triggering as expected here.  
  * We did mute them at a certain point because we knew there was nothing more we could do  
    

---

**Root Cause using [5 Why's methodology](https://xtranet-sonarsource.atlassian.net/wiki/spaces/HELPDESK/pages/2776629308) (**keep asking why until the fundamental cause of a problem is identified):

* Why did AWS go down?  
  us-east-1 had issues in dynamodb which in turn affected a lot of other services  
* Why did it affect SonarQube cloud?  
  We use this region for our US account and also a lot of other services require this region to be up to work, e.g. public ecr.  
* Why did it hit us so hard?  
  Not only do we use this region for our account but a lot of our tools also seem to be hosted in this region. At some point we couldn’t use LaunchDarkly to enable a maintenance window. Even Opsgenie was struggling to send through the alerts.  
* Why do we use this region when it often is the region to have issues?  
  it is the default region to use in US but perhaps we should consider changing region  
  * *To add the reason why this region was chosen when the US instance was set up. (Latency concern)*  
  * *To look into the overall AZ for other US west regions to determine whether it makes sense to switch to another one.*

---

**Remediation Actions (how the incident was mitigated):**

* We had to wait for AWS to solve the issue and then we could see our system start to pick up the slack.  
* We had to manually trigger some ECS tasks to ensure we had the correct workers running.

---

**Caused by a change? Y/N**

* No (not by us at least)

---

**What went well?**

* Our system recovered quite smoothly afterwards  
* Github was still up so we could still implement changes for a code freeze

---

**What did not go so well?**

*  We thought the issue had been mitigated due to the info provided by AWS so we lifted the code freeze but unfortunately issues came flooding back in  
* SPEED was down so I could not run the action to handle the code freeze so we had to implement it manually

---

**Where did we get lucky?**

* So many services were down that there wasn’t really any spotlight on us and the pressure was on AWS.

---

**Preventive / Corrective Actions:**

* [DRAFT: Resourcing Plan for Extended Incident Recovery (Multi-Day, 24/7 Coverage)](https://xtranet-sonarsource.atlassian.net/wiki/x/QQBd9g)  
* **Reassess** the need for the existing **coverage plan** and establish a clear plan for when to trigger this document. @Person2  
* Document the procedure for **muting alarms for a specific environment** (e.g., ProdUS1 during the incident) to allow continuous monitoring of other environments.   
* **Formalize the code freeze actions**. Note: Disabling deployments to a single region is currently challenging but an idea for the future.  
  * The current freeze application time of **45 minutes needs to be optimized**. This requires checking with **EngXP**.  
    * [BUILD-9466: Refreshing state takes too long in re-service-config Closed](https://sonarsource.atlassian.net/browse/BUILD-9466)  
  * Implement a **more formal company communication** (e.g., banner/notification) for these events, as an official channel is lacking. Investigate using the speed action possibility for all these steps.  
  * There is currently **no global view**.  
  * Define the criteria for **initiating the freeze** and for performing the **unfreeze** (e.g., monitoring stability for a determined timeframe).  
* Conduct a **vendor support assessment** for all critical tools.  
  * @Person2  to check the full list of critical tools with @Person3  
    * [MIM-23: Critical Business App \- SQC- Vendor Assessment+ DRPPending](https://sonarsource.atlassian.net/browse/ITOPS-13817)  
  * Add **DRP** to the list of requirements for **PagerDuty/Rootly** (note: it does not exist for OpsGenie). @person4  is to update the moscow matrix.  
  * Check with **Atlassian Statuspage support** if moving to another region is feasible. @Person5  
    * Note: **Bitbucket login was down for EU**, impacting a large category of users.  
* Every squad must check **LaunchDarkly defaults**. Flags are not currently used through IoC. @Person3  
  * **Enhance the ECS runbook**: ECS Fargate Technical Runbook. [ECS Fargate Technical Runbook](https://xtranet-sonarsource.atlassian.net/wiki/x/igBju)  
    * Conduct a **Post-Incident Review** of all pending actions each squad must take (e.g., checking resiliency).  
* **SCA** needs to revisit their **ECS configuration** and follow the Platform instructions. @Person6  
* **Backup-solution**: Review overall AZ for other US west regions to determine if switching to a different one makes sense.

---

**Squads Engaged in the incident:**

* Team-Orange  
* Team-Purple  
* Team-Green  
* Team-Blue  
* Team-Yellow  
* Team-Red  
* Basically all teams were affected.  
* Event on-prem had issues due to docker having issues.

---

**For SonarQube Cloud Incidents, please fill in the details for the following fields. This is needed for** [Service Level Credits](https://www.sonarsource.com/legal/sonarcloud/service-level-agreement/) **calculations:**

* **Region (EU/US/Global): US**  
* **Incident Start Time (CEST):** Provide the incident start time in CEST and provide evidence, such as a log snippet, etc. showing when the incident started.  
  * US: 20th October 9am  
* **Incident Mitigation Time (CEST):** Provide the incident Mitigation time in CEST and provide evidence, such as a log snippet, etc. showing when the incident was mitigated.  
  * US: 20th October 11:40pm  
* **SQC Component:** All in US  
* **Outage Scale:** Full outage

