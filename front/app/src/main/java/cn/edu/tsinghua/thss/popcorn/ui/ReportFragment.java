package cn.edu.tsinghua.thss.popcorn.ui;

import android.app.ProgressDialog;
import android.content.ContentResolver;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Calendar;

import cn.edu.tsinghua.thss.popcorn.MainActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.config.Config;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class ReportFragment extends Fragment {
    private static String ACCESS_TOKEN = "hello_world";
    private static final int TAKE_PICTURE = 1;
    private static final int BROWSE = 2;
    private String REPORT_URL =  Config.LOCAL_IP + "/app/maintain/add/";

    private ProgressDialog progressDialog;

    // 获取sd卡根目录地址,并创建图片父目录文件对象和文件的对象;
    String file_str = Environment.getExternalStorageDirectory().getPath();
    String file_path = file_str + "/willwings/photos";
    File mars_file = new File(file_path);
    File file_go = null;

    @ViewInject(R.id.tab_report_camera)
    private Button cameraButton;

    @ViewInject(R.id.tab_report_browse)
    private Button browseButton;

    @ViewInject(R.id.tab_report_submit_btn)
    private Button submitButton;

    @ViewInject(R.id.tab_report_title)
    private EditText reportTitleText;

    @ViewInject(R.id.tab_report_device_id)
    private EditText deviceIdText;

    @ViewInject(R.id.tab_report_fault_description)
    private EditText faultDescriptionText;

    @ViewInject(R.id.tab_report_memo)
    private EditText reportMemoText;

    @ViewInject(R.id.tab_report_img)
    private ImageView image_view;

    @OnClick(R.id.tab_report_submit_btn)
    private void submitButtonClick(View v){
        String deviceId = deviceIdText.getText().toString();
        String reportTitle = reportTitleText.getText().toString();
        String faultDescription = faultDescriptionText.getText().toString();
        String reportMemo = reportMemoText.getText().toString();
        String imgURL = "";

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", "syb1001");
        params.addBodyParameter("access_token", ACCESS_TOKEN);
        params.addBodyParameter("device_id", deviceId);
        params.addBodyParameter("title", reportTitle);
        params.addBodyParameter("description", faultDescription);
        params.addBodyParameter("image", imgURL);
        params.addBodyParameter("memo", reportMemo);

        progressDialog.setMessage("数据发送中...");
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                REPORT_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {

                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        Toast.makeText(getActivity().getApplicationContext(), responseInfo.result, Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }

                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getActivity().getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }

    @OnClick(R.id.tab_report_camera)
    private void cameraButtonClick(View v){
        if (Environment.MEDIA_MOUNTED.equals(Environment
                .getExternalStorageState())) {
            // 先创建父目录，如果新创建一个文件的时候，父目录没有存在，那么必须先创建父目录，再新建文件。
            boolean isSuccessful = true;
            if (!mars_file.exists()) {
                isSuccessful  = mars_file.mkdirs();
            }
            // 设置跳转的系统拍照的activity为：MediaStore.ACTION_IMAGE_CAPTURE ;
            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            file_go = new File(file_path+"/"+System.currentTimeMillis()+".jpg");
            intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file_go));
            //跳转到拍照界面;
            startActivityForResult(intent, TAKE_PICTURE);
        } else {
            Toast.makeText(getActivity(), "请先安装好SD卡",Toast.LENGTH_LONG).show();
        }
    }

    @OnClick(R.id.tab_report_browse)
    private void browseButtonClick(View v){
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent, BROWSE);
    }

	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
		View reportView = inflater.inflate(R.layout.activity_tab_report, container,false);

        ViewUtils.inject(this, reportView);
        progressDialog = new ProgressDialog(getActivity(), R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(true);

        return reportView;
	}


    //拍照结束后显示图片;
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        // 判断请求码和结果码是否正确，如果正确的话就显示刚刚所拍照的图片;
        if (resultCode == getActivity().RESULT_OK){
            if(requestCode == TAKE_PICTURE){
                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize = 2;
                Bitmap bmpDefaultPic = BitmapFactory.decodeFile(file_go.getPath(), options);
                image_view.setImageBitmap(bmpDefaultPic);
            }else if(requestCode == BROWSE) {
                Uri uri = data.getData();
                ContentResolver cr = getActivity().getContentResolver();
                try {
                    Bitmap bitmap = BitmapFactory.decodeStream(cr.openInputStream(uri));
                    image_view.setImageBitmap(bitmap);
                } catch (FileNotFoundException e) {
                    Log.e("Exception", e.getMessage(),e);
                }
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
	
	@Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}
}
