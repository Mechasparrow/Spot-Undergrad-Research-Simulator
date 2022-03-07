using Assets.SpotControllerScripts.Constants;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasicSpotIssuer : MonoBehaviour
{
    public SpotController spotController;

    // Start is called before the first frame update
    void Start()
    {
        //while (spotController.getControllerReady() != true) { };

        spotController.controllerInitialized += OnSpotControllerReady;
    }

    void OnSpotControllerReady()
    {

        StartCoroutine(SpotControlBasic());

    }

    private IEnumerator SpotControlBasic()
    {
        spotController.UpdateRotation(LegConstants.FRONT_LEFT_UPPER_LEG, SpotState.Go, -45);
        spotController.UpdateRotation(LegConstants.FRONT_LEFT_LOWER_LEG, SpotState.Go, -50);

        spotController.UpdateRotation(LegConstants.FRONT_RIGHT_UPPER_LEG, SpotState.Go, -45);
        spotController.UpdateRotation(LegConstants.FRONT_RIGHT_LOWER_LEG, SpotState.Go, -50);


        spotController.UpdateRotation(LegConstants.REAR_LEFT_UPPER_LEG, SpotState.Go, -45);
        spotController.UpdateRotation(LegConstants.REAR_LEFT_LOWER_LEG, SpotState.Go, -50);


        spotController.UpdateRotation(LegConstants.REAR_RIGHT_UPPER_LEG, SpotState.Go, -45);
        spotController.UpdateRotation(LegConstants.REAR_RIGHT_LOWER_LEG, SpotState.Go, -50);



        yield return new WaitForSeconds(0.2f);

        //spotController.UpdateRotation(LegConstants.FRONT_LEFT_UPPER_LEG, SpotState.Go, 0);
        spotController.UpdateRotation(LegConstants.FRONT_LEFT_LOWER_LEG, SpotState.Go, 0);
        yield return null;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
