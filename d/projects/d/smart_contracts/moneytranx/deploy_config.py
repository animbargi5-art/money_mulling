import logging

import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    from smart_contracts.artifacts.moneytranx.moneytranx_client import (
        MoneytranxFactory,
        SubmitRiskAssessmentArgs,
        GetAccountRiskArgs,
        IsAccountFlaggedArgs,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        MoneytranxFactory, default_sender=deployer_.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        # Fund the contract with 1 ALGO for operations
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )

    # Test the contract functionality
    logger.info(f"AlgoGuard contract deployed successfully!")
    logger.info(f"App ID: {app_client.app_id}")
    logger.info(f"App Address: {app_client.app_address}")
    
    # Test risk assessment functionality
    try:
        # Get stats
        stats_response = app_client.send.get_stats()
        logger.info(f"Contract stats: {stats_response.abi_return}")
        
        # Test account risk check
        risk_response = app_client.send.get_account_risk(
            args=GetAccountRiskArgs(account=deployer_.address)
        )
        logger.info(f"Deployer account risk score: {risk_response.abi_return}")
        
        # Test flagged status
        flagged_response = app_client.send.is_account_flagged(
            args=IsAccountFlaggedArgs(account=deployer_.address)
        )
        logger.info(f"Deployer account flagged: {flagged_response.abi_return}")
        
    except Exception as e:
        logger.warning(f"Contract testing failed: {e}")
        logger.info("Contract deployed but testing incomplete - this is normal for initial deployment")